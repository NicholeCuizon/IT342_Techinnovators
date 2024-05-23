from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse

def accounts_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_email'):
            return HttpResponseRedirect(reverse('login') + '?next=' + request.path)  # Redirect to login URL with next parameter
        return view_func(request, *args, **kwargs)
    return _wrapped_view