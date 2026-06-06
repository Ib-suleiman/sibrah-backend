from django.conf import settings

def site_settings(request):
    """Injects SIBRAH company info into every template."""
    return {
        'COMPANY': settings.SIBRAH_COMPANY,
        'SITE_NAME': 'SIBRAH Computers & Technology Hub',
    }
