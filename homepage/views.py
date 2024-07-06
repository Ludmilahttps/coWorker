from django.conf import settings
from django.utils.translation import activate, get_language, get_language_info
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.db.models import Avg, Count
from .models import Trip, Category, Workspace, WorkspacePhoto, LikedWorkspaces, Notes, Rating, Event
from accounts.models import Users
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import TripForm, WorkspaceForm, ReviewForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.http import Http404
import requests
from geopy.geocoders import GoogleV3
from django.contrib import messages
import setup.settings as GOOGLE_MAPS_API_KEY

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
            'phone_number': request.session.get('phone_number'),
            'is_authenticated': True
        }
    else:
        context['user'] = {
            'name': 'Guest',
            'email': 'guest@example.com',
            'phone_number': _("Not available"),
            'is_authenticated': False
        }

    return context

def error_view(request, exception=None):
    status_code = 500
    error_message = 'An unexpected error occurred.'
    
    if exception:
        status_code = getattr(exception, 'status_code', 500)
        error_message = str(exception)

    context = get_context_data(request)
    context.update({
        'status_code': status_code,
        'error_message': error_message
    })

    return render(request, 'homepage/error.html', context)

def handle_view_errors(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Http404:
            return error_view(args[0], exception=Http404("Page not found"))
        except Users.DoesNotExist:
            raise
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
def add_workspace_view(request):
    if request.method == 'POST':
        form = WorkspaceForm(request.POST, request.FILES)
        if form.is_valid():
            workspace = form.save(commit=False)
            address = request.POST.get('address')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
            location = geolocator.reverse((latitude, longitude), exactly_one=True)
            if location:
                address_components = location.raw.get('address_components', [])
                address_dict = {component['types'][0]: component['long_name'] for component in address_components}

                workspace.country = address_dict.get('country', '')
                workspace.state = address_dict.get('administrative_area_level_1', '')
                workspace.city = address_dict.get('locality', '') or address_dict.get('administrative_area_level_2', '')
                workspace.neighborhood = address_dict.get('sublocality_level_1', '') or address_dict.get('sublocality', '') or address_dict.get('neighborhood', '') or address_dict.get('political', '')
                workspace.street = address_dict.get('route', '')
                workspace.number = address_dict.get('street_number', '')
                workspace.postalCode = address_dict.get('postal_code', '')
                workspace.complement = address_dict.get('subpremise', '')
                workspace.latitude = latitude
                workspace.longitude = longitude

            workspace.save()
            return redirect('discover')
    else:
        form = WorkspaceForm()

    context = {
        'form': form,
    }
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
    reviews = Rating.objects.filter(workspace=workspace)

    if reviews.exists():
        total_reviews = reviews.count()
        overall_rating = reviews.aggregate(Avg('notes__note_general'))['notes__note_general__avg']
        star_counts = {
            i: reviews.filter(notes__note_general=i).count() for i in range(1, 6)
        }
    else:
        total_reviews = 0
        overall_rating = 0
        star_counts = {i: 0 for i in range(1, 6)}

    try:
        notes = Notes.objects.get(workspace=workspace)
    except Notes.DoesNotExist:
        notes = {
            'note_sockets': 1,
            'note_internet': 0,
            'note_silence': 2,
            'note_menu_price': 3,
            'note_daily_price': 5,
            'note_general': 4,
        }

    context = get_context_data(request)
    context.update({
        'workspace': workspace,
        'reviews': reviews,
        'notes': notes,
        'total_reviews': total_reviews,
        'overall_rating': overall_rating,
        'star_counts': star_counts,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

    if request.user.is_authenticated:
        try:
            user = Users.objects.get(email=request.session.get('user_email'))
            liked = LikedWorkspaces.objects.filter(user=user, workspace=workspace).exists()
            context.update({
                'liked': liked
            })
        except Users.DoesNotExist:
            context.update({
                'liked': False
            })
    
    return render(request, 'homepage/workspace_detail.html', context)

@login_required
@handle_view_errors
def add_review_view(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            notes = Notes.objects.create(
                note_general=form.cleaned_data['note_general'],
                note_sockets=form.cleaned_data['note_sockets'],
                note_internet=form.cleaned_data['note_internet'],
                note_silence=form.cleaned_data['note_silence'],
                note_menu_price=form.cleaned_data['note_menu_price'],
                note_daily_price=form.cleaned_data['note_daily_price'],
                workspace=workspace
            )
            review = form.save(commit=False)
            review.user = request.user
            review.workspace = workspace
            review.notes = notes
            review.save()
            return redirect('workspace_detail', workspace_id=workspace.id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'workspace': workspace
    }
    return render(request, 'homepage/add_review.html', context)

@login_required
@handle_view_errors
def vote_review(request, review_id, vote_type):
    review = get_object_or_404(Rating, id=review_id)

    if vote_type == 'upvote':
        review.useful_count += 1
    elif vote_type == 'downvote':
        review.useful_count -= 1
    else:
        return JsonResponse({'success': False, 'error': 'Invalid vote type'}, status=400)

    review.save()
    return JsonResponse({'success': True, 'new_count': review.useful_count})

@handle_view_errors
def get_coordinates(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None