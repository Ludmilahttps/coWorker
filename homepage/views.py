from django.conf import settings
from django.utils.translation import activate, get_language, get_language_info
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from .models import Trip, Category, Workspace, WorkspacePhoto
from .forms import TripForm, WorkspaceForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

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
def discover_view(request):
    categories = Category.objects.all()
    workspaces = Workspace.objects.all()

    context = get_context_data(request)
    context.update({
        'categories': categories,
        'workspaces': workspaces,
    })

    return render(request, 'homepage/discover.html', context)

def add_workspace_view(request, id=None):
    workspace = get_object_or_404(Workspace, id=id) if id else None

    if request.method == 'POST':
        form = WorkspaceForm(request.POST, instance=workspace)
        if form.is_valid():
            form.save()
            return redirect('discover')
    else:
        form = WorkspaceForm(instance=workspace)

    context = get_context_data(request)
    context.update({
        'form': form,
        'workspace': workspace
    })
    return render(request, 'homepage/add_workspace.html', context)

@login_required
def profile_view(request):
    context = get_context_data(request)
    return render(request, 'homepage/profile.html', context)