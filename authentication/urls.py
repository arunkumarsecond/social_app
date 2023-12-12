from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.LoginUserView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_change/', PasswordChangeView.as_view(template_name='authentication/password_change.html', success_url=reverse_lazy('password_change_done')) ),
    path('password_change/done', PasswordChangeDoneView.as_view(template_name='authentication/password_change_done.html'), name='password_change_done')
]