import re
from django.http import JsonResponse
from django.shortcuts import redirect


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.non_auth_paths = ['/user/login/', '/user/login/api/', '/home/', '/sport/', '/about/', '/product/',
                               '/reservation/', '/calendar/api/year/']

    def __call__(self, request):
        # بررسی مسیرهای غیر حفاظتی
        for path in self.non_auth_paths:
            if request.path.startswith(path) or re.match(r'^/your-path/[\d]+/$', request.path):
                return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('user:login')

        return self.get_response(request)
