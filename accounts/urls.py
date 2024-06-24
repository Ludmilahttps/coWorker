from django.urls import path
from .views import login_view, signup_view, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', login_view, name='signin'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', profile_view, name='profile'),
]
