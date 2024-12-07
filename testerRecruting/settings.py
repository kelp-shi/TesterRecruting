import os
from pathlib import Path
from django.contrib import messages
import logging
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    GOOGLE_CLOUD_PROJECT=(str, None),
    USE_GCP_SECRETS=(bool, False),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'django.contrib.sitemaps',
    'baseApp'
]

SITE_ID = 1

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

#media directory
#MEDIA_ROOT = os.path.join(BASE_DIR)
MEDIA_URL = '/contents/'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Load environment variables from .env file
env.read_env(os.path.join(BASE_DIR, ".env"))

#testkey
SECRET_KEY = 'sfsadvnuarjovmncs5485749_143%&fdgbrfbd15646451sefwavcfarehghbr'

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = env("DJANGO_EMAIL")
EMAIL_PORT = env("DJANGO_EMAIL_PORT")
EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", default=False)
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = [env("DJANGO_CONTACT_EMAIL")]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

USE_L10N = False 
DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static')  # ここで静的ファイルが収集されるディレクトリ

WSGI_APPLICATION = 'testerRecruting.wsgi.application'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登録に使用するユーザーモデル
AUTH_USER_MODEL = 'baseApp.CustomUser'

#認証用トークン有効期限
ACTIVATION_TIMEOUT_SECONDS = 60*60*24

SITE_ID = 1 

DEFAULT_PROFILE_IMAGE_PATH = 'baseApp/images/user/profile/defalt.png'

# アプリケーション全体で使用するロガーの設定
logger = logging.getLogger(__name__)

# 使用例
logger.info("アプリケーションが起動しました")
logger.debug("これはデバッグメッセージです")
logger.error("エラーが発生しました", exc_info=True)

#MESSAGE LEVEL
MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger',
    messages.WARNING: 'alert alert-warning',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info'
}

#Login url
LOGIN_URL = 'register/'

DEFAULT_PROFILE_IMAGE_PATH = 'baseApp/static/org/user/profile/defalt.png'

ACTIVATION_TIMEOUT_SECONDS = 60*60*24
