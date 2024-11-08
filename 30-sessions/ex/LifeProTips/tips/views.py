from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tip

import random

User = get_user_model()


def get_or_set_user_name(request):
    now = timezone.now()
    now_timestamp = int(now.timestamp())
    
    expiry_timestamp = request.session.get('user_name_expiry')
    
    if 'user_name' not in request.session or expiry_timestamp is None or now_timestamp > expiry_timestamp:
        request.session['user_name'] = random.choice(settings.USER_NAMES)
        request.session['user_name_expiry'] = now_timestamp + 42
    
    return request.session['user_name']


def get_user_name(request):
    user_name = get_or_set_user_name(request)
    return JsonResponse({'user_name': user_name})


def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
                #clean annonymous session
            request.session.pop('user_name', None)
            request.session.pop('user_name_expiry', None)
            return redirect('homepage')
        else:
            messages.error(request, "Please fix form errors.")
    else:
        form = RegistrationForm()

    return render(request, 'tips/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.pop('user_name', None)
            request.session.pop('user_name_expiry', None)
            return redirect('homepage')
        else:
            messages.error(request, "Credenciales incorrectas.")
    else:
        form = LoginForm()
    return render(request, 'tips/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')


def homepage(request):
    """Displays the homepage with tips and anonymous session management."""
    user_name = get_or_set_user_name(request) if not request.user.is_authenticated else None
    tips = Tip.objects.all().order_by('-date')
    form = TipForm(request.POST or None) if request.user.is_authenticated else None

    # Attach downvote permission to each tip, only if the user is authenticated
    for tip in tips:
        # Check if the user is authenticated and set the downvote permission
        if request.user.is_authenticated:
            # Use the combined permission check on the user
            tip.can_downvote = (request.user == tip.author or request.user.can_downvote_permission())
        else:
            tip.can_downvote = False  # Default to False for anonymous users

    if request.method == 'POST' and form is not None and form.is_valid():
        new_tip = form.save(commit=False)
        new_tip.author = request.user
        new_tip.save()
        return redirect('homepage')

    return render(request, 'tips/homepage.html', {
        'tips': tips,
        'form': form,
        'user_name': user_name,  # Pass anonymous user name to the template
    })



@login_required
def upvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    # Allow upvote for authenticated users
    tip.upvote(request.user)
    return redirect('homepage')


@login_required
def downvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    # Check if user is either the author or has permission based on reputation/upvotes
    if request.user == tip.author or request.user.can_downvote_permission():
        tip.downvote(request.user)
        return redirect('homepage')
    else:
        # Raise permission denied if user lacks downvote privileges
        raise PermissionDenied("You don't have permission to downvote this tip.")

@login_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    # Allows delete if user is the author or has delete permission based on manual or reputation criteria
    if request.user == tip.author or request.user.can_delete_permission():
        tip.delete()
        return redirect('homepage')
    else:
        raise PermissionDenied("You don't have permission to delete this tip.")
