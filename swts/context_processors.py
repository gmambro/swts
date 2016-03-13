def url_info(request):
    """Return useful variables to know the media url and, if you
    need it, your apps url."""

    import settings

    return {
        'BASE_URL' : settings.BASE_URL,
    }

def registry(request):
    from swts.common import registry

    return { 'SWTS_APPS' : registry.app_list() }
