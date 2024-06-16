from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

def signin_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'show_signin': True,
        'show_signup': False,
        'user': request.user if request.user.is_authenticated else AnonymousUser()
    }
    return render(request, 'accounts/sign.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    context = {
        'show_signup': True,
        'show_signin': False,
        'form': form
    }
    return render(request, 'accounts/sign.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def home_view(request):
    context = {
        # Outros contextos que você precisa passar para o template
    }

    if not request.user.is_authenticated:
        request.user = AnonymousUser()

    context['user'] = request.user
    return render(request, 'home.html', context)
