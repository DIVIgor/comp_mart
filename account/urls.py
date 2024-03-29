from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from .forms import LoginForm, PwdResetForm, PwdResetConfirmForm


app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path(
        'activate/<slug:uidb64>/<slug:token>/',
        views.acc_activate, name='activate'
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='account/login/login.html',
            form_class=LoginForm
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/acc/login/'),
        name='logout'
    ),
    # Reset password
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/user/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='account/user/password_reset_email.html',
            form_class=PwdResetForm
        ),
        name='pwd_reset'
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/user/password_reset_confirm.html',
            success_url='/acc/password_reset_complete/',
            form_class=PwdResetConfirmForm
        ),
        name='pwd_reset_confirm'
    ),
    path(
        'password_reset/password_reset_email_confirm/',
        TemplateView.as_view(template_name='account/user/reset_status.html'),
        name='password_reset_done'
    ),
    path(
        'password_reset_complete/',
        TemplateView.as_view(template_name='account/user/reset_status.html'),
        name='password_reset_complete'
        ),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit_info, name='edit_info'),
    path('delete_user/', views.delete_user, name="delete_user"),
    path(
        'delete_confirm/',
        TemplateView.as_view(template_name='account/user/delete_confirm.html'),
        name='delete_confirmation'
    ),
]
