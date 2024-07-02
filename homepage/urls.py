from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover_view, name='discover'),
    path('add_workspace/', views.add_workspace_view, name='add_workspace'),
    path('workspace/<int:workspace_id>/', views.workspace_detail_view, name='workspace_detail'),
    path('like_workspace/<int:workspace_id>/', views.like_workspace, name='like_workspace'),
    path('events/', views.events, name='events'),
    path('trips/', views.trips, name='trips'),
    path('trips/new/', views.new_trip, name='new_trip'),
    path('review/', views.review, name='review'),
    path('about/', views.about, name='about'),
    path('more/', views.more, name='more'),
    path('profile/', views.profile_view, name='profile'),
]
