"""
SIBRAH Production Settings
sibrah_project/settings_production.py
"""

from .settings import *
import os
import dj_database_url

# ── SECURITY ──────────────────────────────────────────────────────────
DEBUG      = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')

ALLOWED_HOSTS = [
    'sibrahtech.com.ng',
    'www.sibrahtech.com.ng',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'https://sibrahtech.com.ng',
    'https://www.sibrahtech.com.ng',
    'https://*.onrender.com',
]

# ── DATABASE ──────────────────────────────────────────────────────────
# Use PostgreSQL on Render, fallback to SQLite locally
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }

# ── STATIC FILES ──────────────────────────────────────────────────────
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL  = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# ── MEDIA FILES ───────────────────────────────────────────────────────
# For production, use cloud storage (Cloudinary) or keep local
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── EMAIL — ZOHO MAIL ─────────────────────────────────────────────────
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.zoho.com'
EMAIL_PORT          = 465
EMAIL_USE_SSL       = True
EMAIL_USE_TLS       = False
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', 'info@sibrahtech.com.ng')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = 'SIBRAH Tech Hub <info@sibrahtech.com.ng>'

# ── SECURITY HEADERS ──────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER        = True
SECURE_CONTENT_TYPE_NOSNIFF      = True
X_FRAME_OPTIONS                  = 'DENY'
SECURE_SSL_REDIRECT               = True
SESSION_COOKIE_SECURE             = True
CSRF_COOKIE_SECURE                = True
SECURE_HSTS_SECONDS               = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS    = True

# ── LOGGING ───────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# ── COMPANY SETTINGS (override with env vars in production) ───────────
SIBRAH_COMPANY = {
    'name':           'SIBRAH Computers & Technology Hub',
    'tagline':        'Empowering Businesses Through Technology, Innovation and Digital Solutions.',
    'phone':          os.environ.get('COMPANY_PHONE', '+234 808 110 1992'),
    'email':          os.environ.get('COMPANY_EMAIL', 'info@sibrahtech.com.ng'),
    'address':        'Abuja, Nigeria',
    'whatsapp':       os.environ.get('COMPANY_WHATSAPP', '2348081101992'),
    'bank_name':      'ACCESS BANK',
    'account_name':   'IBRAHIM BABA SULEIMAN',
    'account_number': '1227425306',
}
