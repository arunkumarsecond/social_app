from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadPostForm
from posts.models import Tag, Post, Comment, PostLike
from django.views.generic import ListView
from users.models import Follow
from django.http import JsonResponse
import re
import json
from django.core.serializers import serialize

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.db.models import Q, Prefetch, F
from django.db import transaction

from django.views import View
from .forms import PostCommentForm

# Create your views here.
class UploadPostView(LoginRequiredMixin, CreateView):
    form_class = UploadPostForm
    template_name = 'mainapp/home.html'
    success_url = '/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        tags = form.cleaned_data['tags'].split(',')
        for tag in tags:
            try:
                # print(tag)
                tag = re.sub(' ', '', tag)
                # print(tag)
                tag_instance = Tag.objects.create(title=tag.lower())
            except:
                tag_instance = Tag.objects.get(title=tag.lower())
            instance.tags.add(tag_instance)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect(reverse('home'))
    
class ListPost(LoginRequiredMixin, ListView):
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        posts = Post.objects.filter(user__username=self.kwargs["username"])
        return posts

    def get(self, request, *args, **kwargs):
        user_followee = Follow.objects.filter(follower=request.user, followee__username=kwargs["username"])
        if request.user.username != kwargs["username"] and user_followee.exists() is False:
            return HttpResponse("404 not found")
        response = super().get(request, *args, **kwargs)
        posts_serialized = serialize("json", response.context_data["object_list"], fields=("image", "uuid"))

        page_obj = response.context_data["page_obj"]

        # check previous page
        if page_obj.has_previous():
            previous = page_obj.previous_page_number()
        else:
            previous = ""

        # check next page
        if page_obj.has_next():
            next = page_obj.next_page_number()
        else:
            next = ""

        return JsonResponse({
            "status": "success",
            "message": "",
            "payload": {
                "count": page_obj.paginator.count,
                "previous": previous,
                "next": next,
                "results": json.loads(posts_serialized)
            }
        })
    
class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.objects.all()
    template_name = "posts/post_detail.html"

    def get_object(self, queryset = None):
        post = self.queryset.filter(
            (Q(user__followers__follower=self.request.user) | Q(user=self.request.user)),
            uuid=self.kwargs["uuid"]
        ).select_related("user", "user__profile").prefetch_related(Prefetch("comments", queryset=Comment.objects.order_by("-created_at").select_related("user", "user__profile")), Prefetch("comments__replies", queryset=Comment.objects.order_by("-created_at").select_related("user", "user__profile"))).distinct().first()
        if post is None:
            raise Http404("Not Foun")
        return post
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        user_post_like = PostLike.objects.filter(user=request.user, post=response.context_data["post"])
        if user_post_like.exists():
            response.context_data["is_liked"] = True
        else:
            response.context_data["is_liked"] = False
        return response

class PostCommentView(LoginRequiredMixin, View):
    form_class = PostCommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() is False:
            return JsonResponse({
                "status": "error",
                "message": "Some error occurred",
                "payload": {
                    "errors": form.errors
                }
            })
        post_uuid = kwargs["uuid"]
        post = Post.objects.filter(
            (Q(user__followers__follower=self.request.user) | Q(user=self.request.user)),
            uuid=self.kwargs["uuid"]
        ).distinct().first()

        if post is None:
            raise Http404("Not Found")
        
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            details=form.cleaned_data["comment_detail"]
        )
        payload = {
            "user": comment.user.username,
            "profile_img": comment.user.profile.profile_img.url,
            "comment_id": comment.id,
            "comment_detail": comment.details
        }
        return JsonResponse({
            "status": "success",
            "message": "Success",
            "payload": payload
        })
    

class LikeDislikePostView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        post_uuid = kwargs["uuid"]
        with transaction.atomic():
            post = Post.objects.filter(
                (Q(user__followers__follower=self.request.user) | Q(user=self.request.user)),
                uuid=self.kwargs["uuid"]
            ).first()

            if post is None:
                raise Http404("Not Found")
            
            post = Post.objects.filter(id=post.id).select_for_update(nowait=True).first()
            post_like = PostLike.objects.filter(post=post, user=request.user).first()

            if post_like is None:
                PostLike.objects.create(
                    post=post,
                    user=request.user
                )
                post.like_count = F("like_count") + 1
                # post.like_count = post.like_count + 1
                post.save()
                is_liked = True
                
            else:
                post_like.delete()
                post.like_count = F("like_count") - 1
                # post.like_count = post.like_count - 1
                post.save()
                is_liked = False

        post.refresh_from_db()
        return JsonResponse({
            "status": "success",
            "message": "",
            "payload": {
                "is_liked": is_liked,
                "like_count": post.like_count
            }
        })