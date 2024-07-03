from django.conf import settings
from django.utils.translation import activate, get_language, get_language_info
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from .models import Trip, Category, Workspace, WorkspacePhoto, LikedWorkspaces
from accounts.models import Users
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import TripForm, WorkspaceForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.http import Http404
import requests

def get_context_data(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    country = 'BR'
    city = 'Unknown'
    language_code = 'pt'

    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            data = response.json()
            country = data.get('country', 'BR')
            city = data.get('city', 'Unknown')
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code.lower() == country.lower():
                    language_code = lang_code
                    break
    except Exception as e:
        print(f"Error obtaining location data: {e}")

    if 'language' in request.GET:
        new_language = request.GET['language']
        activate(new_language)
        request.session['django_language'] = new_language
        return redirect(request.path) 

    current_language = request.session.get('django_language', language_code)
    activate(current_language)

    languages = settings.LANGUAGES
    languages_info = [{'code': lang[0], 'name_local': get_language_info(lang[0])['name_local']} for lang in languages]
    selected_language_name = get_language_info(current_language)['name_local']
    dropdown_visible = request.GET.get('toggle_dropdown') == 'true'

    context = {
        'country': country,
        'city': city,
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
            'type': request.session.get('user_type'),
            'is_authenticated': True
        }
    else:
        context['user'] = {
            'name': 'Guest',
            'email': 'guest@example.com',
            'is_authenticated': False
        }

    return context

def error_view(request, exception=None):
    status_code = 500
    if exception:
        status_code = exception.status_code
        
    context = {
        'status_code': status_code,
        'error_message': exception
    }
    return render(request, 'homepage/error.html', context)

def handle_view_errors(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Http404:
            return error_view(args[0], exception=Http404("Page not found"))
        except Exception as e:
            return error_view(args[0], exception=e)
    return wrapper

@handle_view_errors
def home(request):
    context = get_context_data(request)
    return render(request, 'homepage/discover.html', context)

@handle_view_errors
def events(request):
    context = get_context_data(request)
    return render(request, 'homepage/events.html', context)

@login_required
@handle_view_errors
def review(request):
    user = get_object_or_404(Users, email=request.user.email)
    favorite_workspaces = Workspace.objects.filter(likedworkspaces__user=user)

    context = get_context_data(request)
    context.update({
        'favorite_workspaces': favorite_workspaces
    })

    return render(request, 'homepage/review.html', context)

@handle_view_errors
def about(request):
    context = get_context_data(request)
    return render(request, 'homepage/about.html', context)

@handle_view_errors
def more(request):
    context = get_context_data(request)
    return render(request, 'homepage/more.html', context)

@handle_view_errors
def trips(request):
    current_date = datetime.now().date()
    future_trips = Trip.objects.filter(start_date__gte=current_date).order_by('start_date')
    past_trips = Trip.objects.filter(start_date__lt=current_date).order_by('-start_date')

    context = get_context_data(request)
    context.update({
        'future_trips': future_trips,
        'past_trips': past_trips,
    })

    return render(request, 'homepage/trips.html', context)

@handle_view_errors
def new_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trips')
    else:
        form = TripForm()

    return render(request, 'homepage/new_trip.html', {'form': form})

@handle_view_errors
def discover_view(request):
    categories = Category.objects.all()
    workspaces = Workspace.objects.all()

    context = get_context_data(request)
    context.update({
        'categories': categories,
        'workspaces': workspaces,
    })

    return render(request, 'homepage/discover.html', context)

@handle_view_errors
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

@handle_view_errors
def get_workspace(workspace_id):
    try:
        return Workspace.objects.get(id=workspace_id)
    except Workspace.DoesNotExist:
        return None
    
@login_required
@handle_view_errors
def like_workspace(request, workspace_id):
    print(f"Request to like workspace with ID: {workspace_id}")
    workspace = get_workspace(workspace_id)
    
    if workspace is None:
        print(f"Workspace not found: {workspace_id}")
        return JsonResponse({'success': False, 'error': 'Workspace not found'}, status=404)
    
    print(f"Workspace found: {workspace.name}")
    
    try:
        user = Users.objects.get(email=request.session.get('user_email'))  # Encontra a instância correta do usuário
        liked_workspace, created = LikedWorkspaces.objects.get_or_create(user=user, workspace=workspace)

        if not created:
            liked_workspace.delete()
            is_liked = False
            print(f"Workspace unliked: {workspace_id}")
        else:
            is_liked = True
            print(f"Workspace liked: {workspace_id}")

        return JsonResponse({'success': True, 'isLiked': is_liked}, status=200)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    
@handle_view_errors
def workspace_detail_view(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    context = get_context_data(request)
    context.update({
        'workspace': workspace
    })

    if request.user.is_authenticated:
        user = Users.objects.get(email=request.session.get('user_email'))
        liked = LikedWorkspaces.objects.filter(user=user.id, workspace=workspace_id).exists()
        print(f"liked: {liked}")
        context.update({
            'liked': liked
        })
    
    return render(request, 'homepage/workspace_detail.html', context)

