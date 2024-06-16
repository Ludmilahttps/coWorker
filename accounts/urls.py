from django.urls import path
from .views import signin_view, signup_view, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', signin_view, name='signin'),  # URL para renderizar base.html com signin por padrão
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]
