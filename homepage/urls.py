from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discover/', views.discover, name='discover'),
    path('events/', views.events, name='events'),
    path('trips/', views.trips, name='trips'),
    path('review/', views.review, name='review'),
    path('about/', views.about, name='about'),
    path('more/', views.more, name='more'),
]
