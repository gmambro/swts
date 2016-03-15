from django.http import HttpResponse
from django.template import RequestContext, loader

# using the render_to_response  shortcut without including the RequestContext, 
# prevents context processors from being used in the templates
def make_response(template, request, *args,  **kwargs):
    """Replaces the render_to_response shortcut to use context processors"""

    httpresponse_kwargs = {
        'mimetype': kwargs.pop('mimetype', None),
        }
    kwargs['context_instance'] = RequestContext(request)

    return HttpResponse(loader.render_to_string(template, *args, **kwargs),
                        **httpresponse_kwargs)
