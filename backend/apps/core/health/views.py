from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection


def healthcheck(request):
    db_ok = True
    redis_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        db_ok = False
    try:
        cache.set("healthcheck", "ok", 10)
        cache.get("healthcheck")
    except Exception:
        redis_ok = False
    status_code = 200 if db_ok and redis_ok else 503
    return JsonResponse({"status": "ok" if status_code == 200 else "degraded", "database": db_ok, "redis": redis_ok}, status=status_code)
