from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', view=HomeView.as_view(), name='home')
]