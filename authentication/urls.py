from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetDoneView
urlpatterns = [

    # Sign-up Login, Logout, Activate
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.LoginUserView.as_view(), name = 'login'),
    path('logout/', views.LogoutUserView.as_view(), name="logout"),

    # Password Change
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='authentication/password_change.html',
            success_url=reverse_lazy('password_change_done')
        ),
        name='password_change'
    ),

    path(
        'password_change/done',
        PasswordChangeDoneView.as_view(
            template_name='authentication/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # Password Forget
    path(
        'reset_password/',
        PasswordResetView.as_view(
            template_name="authentication/password_reset.html",
            success_url=reverse_lazy('password_reset_sent'),
            email_template_name='authentication/forgot_password_email.html',
        ),
        name='reset_password'
    ),

    path(
        'reset_password_sent/',
        PasswordChangeDoneView.as_view(
            template_name = "authentication/password_reset_sent.html",
        ),
        name='password_reset_sent'
    ),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='authentication/password_reset_form.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm',
    ),

    path(
        'reset_password_complete',
        PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html",
        ),
        name='password_reset_complete',
    ),

]