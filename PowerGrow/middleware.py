from django.http import JsonResponse


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # کاربر احراز هویت شده است
            return self.get_response(request)
        else:
            # کاربر احراز هویت نشده است
            return JsonResponse({'error': 'Authentication required'}, status=401)
