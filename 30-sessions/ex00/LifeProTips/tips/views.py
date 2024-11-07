import random
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse


def get_or_set_user_name(request):
    now = timezone.now()
    now_timestamp = int(now.timestamp())
    
    expiry_timestamp = request.session.get('user_name_expiry')
    
    if 'user_name' not in request.session or expiry_timestamp is None or now_timestamp > expiry_timestamp:
        request.session['user_name'] = random.choice(settings.USER_NAMES)
        request.session['user_name_expiry'] = now_timestamp + 42
    
    return request.session['user_name']


def homepage(request):
    user_name = get_or_set_user_name(request)
    return render(request, 'tips/homepage.html', {'user_name': user_name})


def get_user_name(request):
    user_name = get_or_set_user_name(request)
    return JsonResponse({'user_name': user_name})
