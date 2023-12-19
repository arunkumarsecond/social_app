from django.urls import path
from .views import GetProfileView, FollowView, UnfollowView
from posts.views import ListPost

urlpatterns = [
    path('profile/<slug:username>/', GetProfileView.as_view(), name='profile'),
    path('users/<slug:username>/follow/', FollowView.as_view(), name='follow'),
    path('users/<slug:username>/unfollow/', UnfollowView.as_view(), name='unfollow'),
    path('users/<slug:username>/posts/', ListPost.as_view(), name='list-user-posts')
]