from django.urls import path
from . import views
from accounts.views import profile_view
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = views.error_view
handler403 = views.error_view
handler404 = views.error_view
handler500 = views.error_view

urlpatterns = [
    path('', views.discover_view, name='discover'),
    path('add_workspace/', views.add_workspace_view, name='add_workspace'),
    path('workspace/<int:workspace_id>/', views.workspace_detail_view, name='workspace_detail'),
    path('workspace/<int:workspace_id>/add_review/', views.add_review_view, name='add_review'),
    path('vote_review/<int:review_id>/<str:vote_type>/', views.vote_review, name='vote_review'),
    path('like_workspace/<int:workspace_id>/', views.like_workspace, name='like_workspace'),
    path('events/', views.events, name='events'),
    path('trips/', views.trips, name='trips'),
    path('trips/new/', views.new_trip, name='new_trip'),
    path('review/', views.review, name='review'),
    path('about/', views.about, name='about'),
    path('more/', views.more, name='more'),
    path('profile/', profile_view, name='profile'),
]
