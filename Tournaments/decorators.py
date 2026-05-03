from functools import wraps
from django.shortcuts import redirect


def player_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if hasattr(request.user, 'founder_profile'):
            return redirect('founder_dashboard')
        if not hasattr(request.user, 'player_profile'):
            return redirect('role_select')
        return view_func(request, *args, **kwargs)
    return wrapper


def founder_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if hasattr(request.user, 'player_profile'):
            return redirect('player_dashboard')
        if not hasattr(request.user, 'founder_profile'):
            return redirect('role_select')
        return view_func(request, *args, **kwargs)
    return wrapper
