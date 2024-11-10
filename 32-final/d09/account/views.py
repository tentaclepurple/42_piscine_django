# account/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def account_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # Return the logged-in context
        return render(request, 'account/account.html',
                     {'username': request.user.username})
    else:
        # Return the login form context
        form = AuthenticationForm()
        return render(request, 'account/account.html', {'form': form})


def ajax_login(request):
    # Handle AJAX login requests
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in if the form is valid
            user = form.get_user()
            login(request, user)
            return JsonResponse({
                'success': True, 
                'username': user.username,
                'redirect_url': '/chat/'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid username or password'
            })


def ajax_logout(request):
    # Handle AJAX logout requests
    if request.method == 'POST' and request.user.is_authenticated:
        # Log the user out if they are authenticated
        logout(request)
        return JsonResponse({
            'success': True,
            'redirect_url': '/chat/'
        })
    return JsonResponse({'success': False})