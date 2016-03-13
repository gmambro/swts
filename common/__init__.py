from django.utils.functional import lazy
from django.core.urlresolvers import reverse

# used because we cannot reverse urls when we are already setting up patterns!
lazy_reverse = lazy(reverse, unicode)
