from django.urls import path
from . import views
from accounts.views import profile_view

urlpatterns = [
    path('', views.home, name='home'),
    path('discover/', views.discover, name='discover'),
    path('events/', views.events, name='events'),
    path('trips/', views.trips, name='trips'),
    path('trips/new/', views.new_trip, name='new_trip'),
    path('review/', views.review, name='review'),
    path('about/', views.about, name='about'),
    path('more/', views.more, name='more'),
    path('profile/', profile_view, name='profile'),
]
