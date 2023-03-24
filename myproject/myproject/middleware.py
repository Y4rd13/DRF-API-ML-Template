from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # only check admin urls
        if request.path.startswith('/admin'):
            # wait until user has been authenticated
            if hasattr(request, 'user') and request.user.is_authenticated:
                # check user account type
                if not (request.user.is_admin and request.user.account_type in ['admin', 'superuser']):
                    messages.error(request, 'You do not have permission to access the administration page.')
                    return redirect(reverse('redoc')) # or other redirect
        return response