from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views


def logout_view(request):
    logout(request)
    return redirect('home')


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
]
