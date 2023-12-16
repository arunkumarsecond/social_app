from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadPostForm
from posts.models import Tag
import re

# Create your views here.
class UploadPostView(CreateView, LoginRequiredMixin):
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
                print('b', tag)
                tag = re.sub(' ', '', tag)
                print('a', tag)
                tag_instance = Tag.objects.create(title=tag.lower())
            except:
                tag_instance = Tag.objects.get(title=tag.lower())
            instance.tags.add(tag_instance)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect(reverse('home'))