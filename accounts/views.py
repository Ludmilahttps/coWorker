from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from .models import Users
from homepage.views import get_context_data
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import activate, get_language, get_language_info


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = Users.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_email'] = user.email
                    request.session['user_type'] = user.type_id

                    context = get_context_data(request)
                    return render(request, 'homepage/home.html', context)
                else:
                    form.add_error('password', 'Password is incorrect')
            except Users.DoesNotExist:
                form.add_error('email', 'Email not found')
    else:
        form = LoginForm()
    return render(request, 'accounts/sign.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign.html', {'form': form, 'show_signup': True})


def home_view(request):
    context = {
        # Outros contextos que você precisa passar para o template
    }

    if not request.user.is_authenticated:
        request.user = AnonymousUser()

    context['user'] = request.user
    return render(request, 'home.html', context)