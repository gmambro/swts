_register = []

def autodiscover():
    from django.conf import settings
    from django.utils.importlib import import_module

    global _register
    _register = []

    for app in settings.INSTALLED_APPS:
        path = app.split(".")
        if path[0] != 'swts':
            continue

        module = import_module(app)
        
        autoreg = getattr(module, 'auto_register', True)
        if autoreg:
            _register.append((path[1], app))

def site_map():
    pass


def patterns():
    from django.conf.urls.defaults import include, url

    list = []

    for r in _register:
        name, app = r
        regex = '^' + name.replace('.', '/') + '/'
        urls = app + '.urls'
        list.append(url(regex, include(urls, namespace=name)))

    return list

def app_list():
    from django.core.urlresolvers import reverse
    return map(lambda x: (x[0], reverse(x[0]+':index')) , _register)
