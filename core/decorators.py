from django.shortcuts import redirect
from django.contrib import messages

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Siz o'qituvchi emassiz!")
        return redirect('core:dashboard')
    return wrapper