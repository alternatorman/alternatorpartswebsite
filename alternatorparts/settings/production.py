import io
import os
from urllib.parse import urlparse

import environ

# Import the original settings from each template
from .base import *

# Load the settings from the environment variable
env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

# Ensure myproject is added to the installed applications
if "alternatorparts" not in INSTALLED_APPS:
    INSTALLED_APPS.append("alternatorparts")

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc,
            "wagtail-cloudrun-313520738970.us-central1.run.app",
            ".alternatorparts.com"]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)

# Set this value from django-environ
DATABASES = {"default": env.db()}
CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://10.204.159.51:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage"
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage"
    }
}


try:
    from .local import *
except ImportError:
    pass
