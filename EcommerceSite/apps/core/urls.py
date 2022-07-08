from django.contrib import admin
from django.urls import path
from django.conf import settings
# from django.contrib.auth import logout
# from django.contrib.auth.views import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required



from core.views import *

app_name = 'core'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('products/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]