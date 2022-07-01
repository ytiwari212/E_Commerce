from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .models import Category

class IndexView(TemplateView):
	template_name = 'index.html' 

# class HomeView(View):
# 	catagaries = Category.objects.all()
# 	def get(self,request, *args, **kwargs):
# 		return render(request, 'index.html',{'catagaries':catagaries})