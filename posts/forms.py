from django.forms import ModelForm
from .models import Post
from django import forms

class UploadPostForm(ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Post
        fields = [
            "image",
            "caption"
        ]

class PostCommentForm(forms.Form):
    comment_detail = forms.CharField(max_length=500)