from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.

class HomeView(View):
    login_required = True
    def get(self, request, *args, **kwargs):
       return render(request, 'mainapp/home.html')