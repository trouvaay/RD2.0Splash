from django.contrib.sites.models import Site


class RefererMiddleware(object):
    """
    Get referring page and store it to the Cookie
    """

    REFERER = 'INITIAL_REFERER'

    def process_request(self, request):
        referer = request.META.get('HTTP_REFERER', '')

        if not self._is_local_domain(referer):
            request.session[RefererMiddleware.REFERER] = referer

    def _is_local_domain(self, url=''):
        site = Site.objects.get_current()
        return site.domain in url
