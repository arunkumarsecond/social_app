from django.urls import path, include
from .views import UploadPostView

urlpatterns = [
    path('', view=UploadPostView.as_view(), name='upload-post'),
]