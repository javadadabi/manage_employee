from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views as accounts_views
from django.urls.base import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path(r'signup/', accounts_views.signup, name='signup'),
    path(r'login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(r'reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url=reverse_lazy("accounts:password_reset_done")
         ),
         name='password_reset'),
    path(r'reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path(r'reset/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path(r'reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path(r'settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                                      success_url=reverse_lazy(
                                                                          "accounts:password_change_done")),
         name='password_change'),
    path(r'settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path(r'update/', accounts_views.UserUpdateView.as_view(), name='my_account'),
    path(r'admin/', admin.site.urls),
]
