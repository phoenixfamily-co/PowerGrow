from django.http import JsonResponse


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # بررسی مسیرهای غیر حفاظتی
        if request.path not in ['/user/login/', '/user/login/api/', '/', '/home/', '/sport/']:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
        return self.get_response(request)