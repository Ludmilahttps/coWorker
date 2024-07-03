from django.urls import path
from .views import login_view, signup_view, home_view, google_login, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('home/', home_view, name='index'),
    path('google/', google_login, name='google_login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
