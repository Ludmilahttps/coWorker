from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, LoginForm
from .models import Users
from homepage.views import get_context_data, discover_view
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import activate, get_language, get_language_info
from django.contrib.auth.backends import ModelBackend

from django.shortcuts import render
from django.views.generic import TemplateView
from setup.settings import YOUR_GOOGLE_CLIENT_ID

import json
import time
from django.utils import timezone
import logging
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from google.oauth2 import id_token
from google.auth.transport import requests

logger = logging.getLogger(__name__)

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             try:
#                 user = Users.objects.get(email=email)
#                 if user.check_password(password):
#                     request.session['user_id'] = user.id
#                     request.session['user_name'] = user.name
#                     request.session['user_email'] = user.email
#                     request.session['user_type'] = user.type_id

#                     context = get_context_data(request)
#                     # return discover_view(request)
#                     return render(request, 'homepage/discover.html', context)
#                 else:
#                     form.add_error('password', 'Password is incorrect')
#             except Users.DoesNotExist:
#                 form.add_error('email', 'Email not found')
#     else:
#         form = LoginForm()
#     return render(request, 'accounts/sign.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = Users.objects.get(email=email)
                if user.check_password(password):
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_email'] = user.email
                    request.session['user_type'] = user.type_id

                    # Autenticar o usuário manualmente
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)

                    next_url = request.GET.get('next', 'discover')
                    return redirect(next_url)
                else:
                    form.add_error('password', 'Password is incorrect')
            except Users.DoesNotExist:
                form.add_error('email', 'Email not found')
    else:
        form = LoginForm()
    return render(request, 'accounts/sign.html', {'form': form})

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['YOUR_GOOGLE_CLIENT_ID'] = YOUR_GOOGLE_CLIENT_ID
        return context

@csrf_exempt
def google_login(request):
    if request.method != 'POST':
        logger.error("Requisição GET recebida em vez de POST")
        return HttpResponseBadRequest("Requisição inválida")

    logger.debug("Recebendo requisição POST para login com Google")
    logger.debug(f"Requisição: {request}")
    logger.debug(f"Corpo da requisição: {request.body}")
    
    try:
        body = request.body.decode('utf-8')
        logger.debug(f"Corpo da requisição decodificado: {body}")

        token_data = json.loads(body)
        token = token_data.get('id_token')
        if not token:
            logger.error("Token não encontrado na requisição")
            return HttpResponseBadRequest("Token não encontrado")
        
        logger.debug(f"Token recebido: {token}")

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        logger.info(f"Informações do usuário: {idinfo}")

        return JsonResponse({'status': 'success', 'userid': userid})
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return HttpResponseBadRequest("Erro ao decodificar JSON")
    except ValueError as e:
        logger.error(f"Erro ao verificar o token: {e}")
        return HttpResponseBadRequest("Token inválido")
    except KeyError:
        logger.error("Chave 'id_token' não encontrada na requisição")
        return HttpResponseBadRequest("Token não encontrado")

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data['password'])
#             user.save()
#             return redirect('login')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/sign.html', {'form': form, 'show_signup': True})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            
            # Log in the user after signing up
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_email'] = user.email
                request.session['user_type'] = user.type_id

                next_url = request.GET.get('next', 'discover')
                return redirect(next_url)
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign.html', {'form': form, 'show_signup': True})


def home_view(request):
    if not request.user.is_authenticated:
        request.user = AnonymousUser()

    context = {
        'YOUR_GOOGLE_CLIENT_ID': YOUR_GOOGLE_CLIENT_ID,
        'user': request.user,
    }
    return render(request, "accounts/index.html", context)
