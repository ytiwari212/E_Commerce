from django.shortcuts import render
# from django.view import View
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
	template_name = 'index.html' 