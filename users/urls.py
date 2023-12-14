from django.urls import path
from .views import GetProfileView, FollowView, UnfollowView

urlpatterns = [
    path('profile/<slug:username>/', GetProfileView.as_view(), name='profile'),
    path('users/<slug:username>/follow', FollowView.as_view(), name='follow'),
    path('users/<slug:username>/unfollow', UnfollowView.as_view(), name='unfollow'),
]