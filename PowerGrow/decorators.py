# decorators.py
from functools import wraps
from django.http import JsonResponse


def session_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({'error': 'Authentication required'}, status=401)
    return _wrapped_view
