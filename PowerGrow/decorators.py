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


def session_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_teacher or request.user.is_superuser or
                                              request.user.is_staff):
            return view_func(request, *args, **kwargs)
        return redirect('user:login')
    return _wrapped_view


def session_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return view_func(request, *args, **kwargs)
        return redirect('user:login')
    return _wrapped_view


def session_staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('user:login')
    return _wrapped_view
