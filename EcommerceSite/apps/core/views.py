from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from .models import Category,Product,Order
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages




class IndexView(View):

	def post(self , request):
		product = request.POST.get('product')
		remove = request.POST.get('remove')
		cart = request.session.get('cart')
		if cart:
		    quantity = cart.get(product)
		    if quantity:
		        if remove:
		            if quantity<=1:
		                cart.pop(product)
		            else:
		                cart[product]  = quantity-1
		        else:
		            cart[product]  = quantity+1

		    else:
		        cart[product] = 1
		else:
		    cart = {}
		    cart[product] = 1

		request.session['cart'] = cart
		print('cart' , request.session['cart'])
		return redirect('core:index')

	def get(self , request):

		return HttpResponseRedirect(f'products/{request.get_full_path()[1:]}')


def user_logout(request):
	logout(request)
	return redirect('core:home')


class HomeView(View):

	def get(self,request, *args, **kwargs):
		catagaries = Category.objects.all()
		products = Product.objects.all()
		return render(request, 'index.html',{'catagaries':catagaries,'products':products})



class ProductView(View):

	# def get(self,request, pk):
	# 	# breakpoint()
	# 	catagaries = Category.objects.all()
	# 	catagary = Category.objects.filter(pk=pk).last()
	# 	products = Product.objects.filter(category=catagary)
	# 	return render(request, 'index.html',{'catagaries':catagaries,'products':products})


	def get(self,request):
	    data = {}
	    cart = request.session.get('cart')
	    if not cart:
	        request.session['cart'] = {}
	    products = None
	    categories = Category.get_all_categories()
	    categoryID = request.GET.get('category')
	    if categoryID:
	        products = Product.objects.filter(category=categoryID)
	    else:
	        products = Product.objects.all()

	    data['products'] = products
	    data['categories'] = categories

	    return render(request, 'index.html', data)


class RegistrationView(View):
	def get(self,request, *args, **kwargs):
		form = RegistrationForm()
		return render(request, 'signup.html',{'form':form})

	def post(self, request, *args, **kwargs):
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.data['password'])
			user.save()
			messages.success(request, 'User Registered Successfully')
			return redirect('core:login')
		else:
			messages.error(request, form.errors)
			return HttpResponseRedirect('/signup/')
		return render(request, 'signup.html',{'form':form})



class LoginView(View):
	def get(self,request, *args, **kwargs):
		form = LoginForm()
		return render(request, 'login.html',{'form':form})

	def post(self, request, *args, **kwargs):
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				# message = f'Hello {user.username}! You have been logged in'
				return redirect('core:home')
			else:
				message = 'Please provide valid username and password'
				messages.error(request, message)
				return redirect('core:login')
		else:
			messages.error(request, form.errors)
			return redirect('core:login')


class CartView(View):

    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request , 'cart.html' , {'products' : products} )


class CheckOut(View):

	def post(self, request):
		address = request.POST.get('address')
		phone = request.POST.get('phone')
		# customer = request.session.get('customer')
		cart = request.session.get('cart')
		products = Product.objects.filter(id__in=cart.keys())
		for product in products:
			order = Order.objects.create(customer=request.user,
						product=product,
						price=product.price,
						address=address, 
						phone=phone, 
						quantity=cart.get(str(product.id)),
						status='Panding'
						) 
			order.save()
		request.session['cart'] = {}
		return redirect('core:cart')