import io
import os
from pathlib import Path
from django.contrib import messages
from urllib.parse import urlparse
import environ
import google.auth
from google.cloud import secretmanager



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 環境変数の読み込み
env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

# Cloud Run の環境変数設定
env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")
print("SECRET_KEY:", os.environ.get("SECRET_KEY"))
# Attempt to load the Project ID into the environment, safely failing on error.
print("アクセス開始")
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
    print("アクセス")
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    print("ローカル参照")
    # Use a local secret file, if provided

    env.read_env(env_file)
# [START_EXCLUDE]
elif os.getenv("TRAMPOLINE_CI", None):
    print("Ci実行")
    # Create local settings if running with CI, for unit testing

    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    print("GOOGLE_CLOUD_PROJECT実行")
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "terec_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END cloudrun_django_secret_config]
SECRET_KEY = env("SECRET_KEY")
print("secret_key=", os.environ.get("SECRET_KEY"))

DEBUG = env("DEBUG")
print("debug=", os.environ.get("DEBUG"))

# Cloud Run 特有の設定
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'baseApp',
    'storages',  # 追加：Google Cloud Storage 用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'testerRecruting.middleware.AdminPermissionMiddleware',
]

ROOT_URLCONF = 'testerRecruting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATIC_URL = '/static/'
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'BUCKET_NAME': GS_BUCKET_NAME,
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'BUCKET_NAME': GS_BUCKET_NAME,
    },
}
GS_DEFAULT_ACL = 'publicRead'

# WSGI
WSGI_APPLICATION = 'testerRecruting.wsgi.application'
print("---DB接続----")
# Database settings
DATABASES = {"default": env.db()}

print("---DB接続proxy判定----", os.getenv("USE_CLOUD_SQL_AUTH_PROXY"))
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    print("----USE_CLOUD_SQL_AUTH_PROXY----")
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("DJANGO_EMAIL")
EMAIL_PORT = os.environ.get("DJANGO_EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS")
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = [os.environ.get("DJANGO_CONTACT_EMAIL")]

# その他の設定
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'baseApp.CustomUser'
MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger',
    messages.WARNING: 'alert alert-warning',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info'
}

LOGIN_URL = 'register/'

DEFAULT_PROFILE_IMAGE_PATH = 'baseApp/images/user/profile/defalt.png'

ACTIVATION_TIMEOUT_SECONDS = 60*60*24
