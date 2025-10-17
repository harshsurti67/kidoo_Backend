from .settings import *  # noqa

# Override only the DATABASES to point to the local SQLite file for export
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # type: ignore[name-defined]
    }
}

# Keep DEBUG minimal to avoid noisy outputs during export
DEBUG = False


