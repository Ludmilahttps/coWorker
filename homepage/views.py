from django.conf import settings
from django.utils.translation import activate, get_language, get_language_info
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from .models import Trip, Category, Workspace
from .forms import TripForm
from django.utils.translation import gettext as _

def get_context_data(request):
    if 'language' in request.GET:
        new_language = request.GET['language']
        activate(new_language)
        request.session['django_language'] = new_language
        return redirect(request.path) 

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

    if 'user_id' in request.session:
        context['user'] = {
            'id': request.session.get('user_id'),
            'name': request.session.get('user_name'),
            'email': request.session.get('user_email'),
            'type': request.session.get('user_type')
        }
    else:
        context['user'] = {
            'name': 'Guest',
            'email': 'guest@example.com'
        }

    return context

def home(request):
    context = get_context_data(request)
    return render(request, 'homepage/home.html', context)

def events(request):
    context = get_context_data(request)
    return render(request, 'homepage/events.html', context)

def review(request):
    context = get_context_data(request)
    return render(request, 'homepage/review.html', context)

def about(request):
    context = get_context_data(request)
    return render(request, 'homepage/about.html', context)

def more(request):
    context = get_context_data(request)
    return render(request, 'homepage/more.html', context)

def trips(request):
    if 'language' in request.GET:
        new_language = request.GET['language']
        activate(new_language)
        request.session['django_language'] = new_language
        return redirect('/')

    current_language = request.session.get('django_language', get_language())
    activate(current_language)

    languages = settings.LANGUAGES
    languages_info = [{'code': lang[0], 'name_local': get_language_info(lang[0])['name_local']} for lang in languages]
    selected_language_name = get_language_info(current_language)['name_local']
    dropdown_visible = request.GET.get('toggle_dropdown') == 'true'

    current_date = datetime.now().date()
    future_trips = Trip.objects.filter(start_date__gte=current_date).order_by('start_date')
    past_trips = Trip.objects.filter(start_date__lt=current_date).order_by('-start_date')

    context = {
        'future_trips': future_trips,
        'past_trips': past_trips,
        'selected_language': current_language,
        'selected_language_name': selected_language_name,
        'languages': languages_info,
        'dropdown_visible': dropdown_visible
    }
    return render(request, 'homepage/trips.html', context)

def new_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trips')
    else:
        form = TripForm()

    return render(request, 'homepage/new_trip.html', {'form': form})

# Discover screen
def discover(request):
    Categories = Category.objects.all()
    Workspaces = Workspace.objects.all()
    context = {
        'categories': Categories,
        'workspaces': Workspaces,
        'selected_language': request.LANGUAGE_CODE,
        'selected_language_name': request.LANGUAGE_CODE,
        'dropdown_visible': False,
    }
    return render(request, 'homepage/discover.html', context)