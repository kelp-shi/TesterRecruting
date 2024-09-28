import logging
from django.http import HttpResponseForbidden
from django.urls import reverse

logger = logging.getLogger(__name__)

class AdminPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            admin_url = reverse('admin:index')
            logger.debug(f'Admin URL: {admin_url}')
            if request.path.startswith(admin_url):
                if not request.user.is_superuser:
                    logger.debug('User is not superuser, returning 403')
                    return HttpResponseForbidden()
        except Exception as e:
            logger.error(f'Error in AdminPermissionMiddleware: {e}')
            raise e
        response = self.get_response(request)
        return response