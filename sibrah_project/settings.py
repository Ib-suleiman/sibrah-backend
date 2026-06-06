"""
SIBRAH Computers & Technology Hub
Django Settings - sibrah_project/settings.py
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'sibrah-change-this-secret-key-in-production-2025'

DEBUG = True

ALLOWED_HOSTS = ['*']

# ── INSTALLED APPS ──
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'rest_framework',
    'django_filters',

    # SIBRAH Apps
    'apps.core',
    'apps.accounts',
    'apps.training',
    'apps.shop',
    'apps.certificates',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'sibrah_project.urls'

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
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'sibrah_project.wsgi.application'

# ── DATABASE ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sibrah.db',
    }
}

# ── AUTH ──
AUTH_USER_MODEL = 'accounts.SibrahUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# ── ALLAUTH ──
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/portal/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# ── INTERNATIONALISATION ──
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# ── STATIC & MEDIA ──
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── CRISPY FORMS ──
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ── EMAIL (console for development) ──
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'SIBRAH Tech Hub <info@sibrahtech.com.ng>'

# ── COMPANY SETTINGS ──
SIBRAH_COMPANY = {
    'name': 'SIBRAH Computers & Technology Hub',
    'tagline': 'Empowering Businesses Through Technology, Innovation and Digital Solutions.',
    'phone': '+234 808 110 1992',
    'email': 'info@sibrahtech.com.ng',
    'address': 'Abuja, Nigeria',
    'whatsapp': '2348081101992',
    'bank_name': 'ACCESS BANK',
    'account_name': 'IBRAHIM BABA SULEIMAN',
    'account_number': '1227425306',
}

# ── REST FRAMEWORK ──
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}
