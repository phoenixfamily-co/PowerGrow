# decorators.py
from functools import wraps
from django.shortcuts import redirect


def session_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('user:login')
    return _wrapped_view
