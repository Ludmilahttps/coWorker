from django.conf import settings
from django.utils.translation import activate, get_language, get_language_info
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser

def get_context_data(request):
    if 'language' in request.GET:
        new_language = request.GET['language']
        activate(new_language)
        request.session['django_language'] = new_language
        return redirect(request.path)  # redirecionar para a mesma página

    current_language = request.session.get('django_language', get_language())
    activate(current_language)

    languages = settings.LANGUAGES
    languages_info = [{'code': lang[0], 'name_local': get_language_info(lang[0])['name_local']} for lang in languages]
    selected_language_name = get_language_info(current_language)['name_local']
    dropdown_visible = request.GET.get('toggle_dropdown') == 'true'

    context = {
        'country': 'Brazil',
        'selected_language': current_language,
        'selected_language_name': selected_language_name,
        'languages': languages_info,
        'dropdown_visible': dropdown_visible
    }

    if not request.user.is_authenticated:
        request.user = AnonymousUser()

    context['user'] = request.user

    return context

def home(request):
    context = get_context_data(request)
    return render(request, 'homepage/home.html', context)

def discover(request):
    context = get_context_data(request)
    return render(request, 'homepage/discover.html', context)

def events(request):
    context = get_context_data(request)
    return render(request, 'homepage/events.html', context)

def trips(request):
    context = get_context_data(request)
    return render(request, 'homepage/trips.html', context)

def review(request):
    context = get_context_data(request)
    return render(request, 'homepage/review.html', context)

def about(request):
    context = get_context_data(request)
    return render(request, 'homepage/about.html', context)

def more(request):
    context = get_context_data(request)
    return render(request, 'homepage/more.html', context)
