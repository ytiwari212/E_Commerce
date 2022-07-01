from django.contrib import admin
from django.urls import path
from core.views import IndexView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index-view'),
]