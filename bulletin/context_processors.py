from django.conf import settings


def site_config(request):
    """Add site configuration to all template contexts."""
    return {
        'CITY_NAME': settings.CITY_NAME,
        'CITY_STATE': settings.CITY_STATE,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
    }
