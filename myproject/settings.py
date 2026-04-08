from pathlib import Path
from google.cloud import secretmanager
import dj_database_url
import os

def get_secret(secret_id):
    if os.environ.get('GAE_ENV') == 'standard':
        try:
            client = secretmanager.SecretManagerServiceClient()
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
            name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception:
            return os.environ.get(secret_id)
    
    return os.environ.get(secret_id)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'ideiglenes-kulcs-fejleszteshez')
DEBUG = os.environ.get('GAE_ENV') != 'standard'
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photos',
    'storages', # Google Cloud Storage-hoz kell
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# --- DATABASE CONFIGURATION ---
# If on App Engine, use Secret Manager. If local, check for DATABASE_URL env var.
if os.environ.get('GAE_ENV') == 'standard':
    DATABASE_URL = get_secret('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    # Local development: use Neon if DATABASE_URL is set, otherwise fallback to SQLite
    local_db_url = os.environ.get('DATABASE_URL')
    if local_db_url:
        DATABASES = {
            'default': dj_database_url.config(default=local_db_url, conn_max_age=600, ssl_require=True)
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# --- STORAGE CONFIGURATION ---
# Terraform managed bucket name
GS_BUCKET_NAME = 'gallery-488215-images-iac'

if os.environ.get('GAE_ENV') == 'standard' or os.environ.get('USE_CLOUD_STORAGE') == 'true':
    GS_QUERYSTRING_AUTH = False
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files settings
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Auth settings
LOGOUT_METHODS = ('GET', 'POST')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]