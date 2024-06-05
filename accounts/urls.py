from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import profile
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]
