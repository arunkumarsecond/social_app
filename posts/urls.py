from django.urls import path, include
from .views import UploadPostView, PostDetailView, PostCommentView, LikeDislikePostView

urlpatterns = [
    path('', view=UploadPostView.as_view(), name='upload-post'),
    path('<slug:uuid>/', view=PostDetailView.as_view(), name="post-detail"),
    path("<slug:uuid>/comments/", PostCommentView.as_view(), name="post-comment"),
    path("<slug:uuid>/like_dislike/", LikeDislikePostView.as_view(), name='post-like-dislike')
]
