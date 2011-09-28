r"""

    occupywallst.middleware
    ~~~~~~~~~~~~~~~~~~~~~~~

    Django middleware definitions.

"""

import traceback

from django.db import connection
from django.template import Template, Context
from django.utils.cache import add_never_cache_headers


class PrintException(object):
    def process_exception(self, request, exception):
        traceback.print_exc()


class NeverCache(object):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class XForwardedForMiddleware(object):
    """Replace ``REMOTE_ADDR`` with ``HTTP_X_FORWARDED_FOR``

    When reverse proxying from nginx, we receive a tcp connection from
    localhost which isn't the client's real ip address.  Normally
    reverse proxies are configured to set the ``X-Forwarded-For``
    header which gives us the actual client ip.
    """

    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
            request.META['REMOTE_HOST'] = None
