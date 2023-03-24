import os
from os.path import join, dirname
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Authentication user model
AUTH_USER_MODEL = 'myapp.CustomUser'

# The environment the app runs in: development/production/test etc.
APP_ENV = os.getenv('APP_ENV', 'development')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

if APP_ENV == 'production':
    DEBUG = False
    ALLOWED_HOSTS = ['my-domain.com']
elif APP_ENV == 'development':
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# Don't allow credentials via CORS as this API is designed to be
# stateless and shouldn't rely on cookies
CORS_ALLOW_CREDENTIALS = False

# Since the service doesn't rely on cookies, it is okay to allow all origins
CORS_ORIGIN_ALLOW_ALL = True

# Celery settings
CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL') # "redis://localhost:6379"
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC' # List of timezones available: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
CELERY_ENABLE_UTC = True
CELERY_CONCURRENCY = int(os.getenv('CELERY_CONCURRENCY'))

# RSA settings
RSA_PUBLIC_KEY = os.getenv('RSA_PUBLIC_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework',
    'drf_yasg',
    'myapp',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # In case you want to use throttling, uncomment the following lines:
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     #'SysRecIS.throttling.CustomThrottle',
    #     'rest_framework.throttling.ScopedRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'SysRecApp': '1/second',
    # }
}

# Swagger settings
SWAGGER_SETTINGS = {
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.ReferencingSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.JSONFieldInspector',
        'drf_yasg.inspectors.HiddenFieldInspector',
        'drf_yasg.inspectors.RecursiveFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
    'SECURITY_DEFINITIONS': {
        'Auth Token [Bearer {JWT}]': {  # api_key
            # Required. The type of the security scheme. Valid values are "basic", "apiKey" or "oauth2"
            'type': 'apiKey',
            # Required. The name of the header or query parameter to be used.
            'name': 'Authorization',
            'in': 'header',  # Required The location of the API key. Valid values are "query" or "header"
        }
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=2),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'RS256',
    'SIGNING_KEY': os.getenv('RSA_PRIVATE_KEY'),
    'VERIFYING_KEY': os.getenv('RSA_PUBLIC_KEY'),
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'uid',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'myproject.middleware.AdminPermissionMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database (used only to store the user credentials)
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT_PATH = Path(__file__).resolve().parent.parent.parent # os.path.dirname(__file__)
STATIC_ROOT = os.path.join(STATIC_ROOT_PATH, 'assets/static/')
STATICFILES_DIRS = [os.path.join(STATIC_ROOT_PATH, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
