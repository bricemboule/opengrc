from __future__ import annotations

from decimal import Decimal, InvalidOperation
from functools import lru_cache
from math import asin, cos, radians, sin, sqrt

from django.conf import settings
from django.db import connection
from django.db.models import QuerySet


def to_float(value):
    if value in (None, ""):
        return None
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError, InvalidOperation):
        return None


def build_point_geometry(latitude, longitude):
    latitude_value = to_float(latitude)
    longitude_value = to_float(longitude)
    if latitude_value is None or longitude_value is None:
        return None

    return {
        "type": "Point",
        "coordinates": [round(longitude_value, 6), round(latitude_value, 6)],
    }


def sync_point_geometry(instance, *, lat_field="latitude", lng_field="longitude", geometry_field="geometry_geojson"):
    if not hasattr(instance, geometry_field):
        return
    setattr(
        instance,
        geometry_field,
        build_point_geometry(getattr(instance, lat_field, None), getattr(instance, lng_field, None)),
    )


def normalize_point_payload(attrs, instance=None, *, lat_field="latitude", lng_field="longitude", geometry_field="geometry_geojson"):
    latitude = attrs.get(lat_field, getattr(instance, lat_field, None) if instance else None)
    longitude = attrs.get(lng_field, getattr(instance, lng_field, None) if instance else None)
    attrs[geometry_field] = build_point_geometry(latitude, longitude)
    return attrs


def parse_bbox(value):
    if not value:
        return None
    try:
        min_lng, min_lat, max_lng, max_lat = [float(part.strip()) for part in str(value).split(",")]
    except (TypeError, ValueError):
        return None
    return min_lng, min_lat, max_lng, max_lat


def haversine_km(lat1, lng1, lat2, lng2):
    radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    origin_lat = radians(lat1)
    target_lat = radians(lat2)

    arc = sin(d_lat / 2) ** 2 + cos(origin_lat) * cos(target_lat) * sin(d_lng / 2) ** 2
    return 2 * radius * asin(sqrt(arc))


def filter_queryset_by_bbox(queryset: QuerySet, bbox, *, lat_field="latitude", lng_field="longitude"):
    parsed = parse_bbox(bbox)
    if not parsed:
        return queryset

    min_lng, min_lat, max_lng, max_lat = parsed
    return queryset.filter(
        **{
            f"{lng_field}__isnull": False,
            f"{lat_field}__isnull": False,
            f"{lng_field}__gte": min_lng,
            f"{lng_field}__lte": max_lng,
            f"{lat_field}__gte": min_lat,
            f"{lat_field}__lte": max_lat,
        }
    )


def filter_queryset_by_radius(queryset: QuerySet, *, near_lat, near_lng, radius_km, lat_field="latitude", lng_field="longitude"):
    origin_lat = to_float(near_lat)
    origin_lng = to_float(near_lng)
    radius_value = min(to_float(radius_km) or settings.SPATIAL_ANALYSIS_DEFAULT_RADIUS_KM, settings.SPATIAL_ANALYSIS_MAX_RADIUS_KM)

    if origin_lat is None or origin_lng is None:
        return queryset

    records = queryset.filter(**{f"{lat_field}__isnull": False, f"{lng_field}__isnull": False})
    matching_ids = []
    for item in records.only("id", lat_field, lng_field):
        distance = haversine_km(origin_lat, origin_lng, to_float(getattr(item, lat_field)), to_float(getattr(item, lng_field)))
        if distance <= radius_value:
            matching_ids.append(item.id)
    return queryset.filter(id__in=matching_ids)


@lru_cache(maxsize=1)
def spatial_backend_summary():
    if connection.vendor != "postgresql":
        return {"enabled": False, "engine": connection.settings_dict.get("ENGINE", ""), "postgis": False}

    enabled = connection.settings_dict.get("ENGINE") == "django.contrib.gis.db.backends.postgis"
    postgis = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis')")
            postgis = bool(cursor.fetchone()[0])
    except Exception:
        postgis = False

    return {
        "enabled": enabled,
        "engine": connection.settings_dict.get("ENGINE", ""),
        "postgis": postgis,
        "srid": getattr(settings, "SPATIAL_REFERENCE_SRID", 4326),
    }


def apply_spatial_filters(queryset: QuerySet, request, *, lat_field="latitude", lng_field="longitude"):
    bbox = request.query_params.get("bbox")
    near_lat = request.query_params.get("near_lat")
    near_lng = request.query_params.get("near_lng")
    radius_km = request.query_params.get("radius_km")

    if bbox:
        queryset = filter_queryset_by_bbox(queryset, bbox, lat_field=lat_field, lng_field=lng_field)

    if near_lat and near_lng:
        queryset = filter_queryset_by_radius(
            queryset,
            near_lat=near_lat,
            near_lng=near_lng,
            radius_km=radius_km,
            lat_field=lat_field,
            lng_field=lng_field,
        )

    return queryset


def build_feature_collection(rows, *, title_field="name", lat_field="latitude", lng_field="longitude", status_field="status"):
    features = []
    for row in rows:
        latitude = to_float(row.get(lat_field))
        longitude = to_float(row.get(lng_field))
        if latitude is None or longitude is None:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry": build_point_geometry(latitude, longitude),
                "properties": {
                    "id": row.get("id"),
                    "title": row.get(title_field) or row.get("title") or row.get("code") or f"Record {row.get('id')}",
                    "status": row.get(status_field),
                    "sector": row.get("sector") or row.get("target_sector") or row.get("admin_area"),
                    "location": row.get("location") or row.get("admin_area"),
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}
