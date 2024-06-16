from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def signin_view(request):
    context = {
        'show_signin': True,
        'show_signup': False
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
