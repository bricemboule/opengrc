import socket
from urllib.parse import urlsplit, urlunsplit

from .base import *

DEBUG = True


def _host_is_resolvable(host):
    try:
        socket.getaddrinfo(host, None)
        return True
    except socket.gaierror:
        return False


def _swap_service_host(url, source_host, target_host):
    parts = urlsplit(url)
    if parts.hostname != source_host:
        return url

    auth = ""
    if parts.username:
        auth = parts.username
        if parts.password:
            auth = f"{auth}:{parts.password}"
        auth = f"{auth}@"

    port = f":{parts.port}" if parts.port else ""
    netloc = f"{auth}{target_host}{port}"
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


if DATABASES["default"].get("HOST") == "db" and not _host_is_resolvable("db"):
    DATABASES["default"]["HOST"] = "127.0.0.1"

if REDIS_URL and urlsplit(REDIS_URL).hostname == "redis" and not _host_is_resolvable("redis"):
    REDIS_URL = _swap_service_host(REDIS_URL, "redis", "127.0.0.1")
    CACHES["default"]["LOCATION"] = REDIS_URL

if CELERY_BROKER_URL and urlsplit(CELERY_BROKER_URL).hostname == "redis" and not _host_is_resolvable("redis"):
    CELERY_BROKER_URL = _swap_service_host(CELERY_BROKER_URL, "redis", "127.0.0.1")

if CELERY_RESULT_BACKEND and urlsplit(CELERY_RESULT_BACKEND).hostname == "redis" and not _host_is_resolvable("redis"):
    CELERY_RESULT_BACKEND = _swap_service_host(CELERY_RESULT_BACKEND, "redis", "127.0.0.1")

if CHANNEL_REDIS_URL and urlsplit(CHANNEL_REDIS_URL).hostname == "redis" and not _host_is_resolvable("redis"):
    CHANNEL_REDIS_URL = _swap_service_host(CHANNEL_REDIS_URL, "redis", "127.0.0.1")
    CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [CHANNEL_REDIS_URL]
