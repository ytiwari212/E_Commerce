import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from .models import Category, Product, Order, OrderProduct,Coupon
from .forms import RegistrationForm, LoginForm,CouponForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import get_template
from .utils import order_confirmation_mail
from django.utils import timezone
from .templatetags.cart import total_cart_price
from django.db.models import F



today = datetime.date.today()


class IndexView(View):
    def post(self, request):
        # product = request.POST.get("product")
        cart_product = request.POST.get("cart_product")
        home_product = request.POST.get("home_product")
        delete_product = request.POST.get('delete_product')
        remove = request.POST.get("remove")
        cart = request.session.get("cart")

        if delete_product:
        	del request.session.get("cart")[delete_product]
        	request.session.modified = True
        	return redirect("core:cart")
        product = home_product if home_product else cart_product
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session["cart"] = cart
        if home_product:
        	return redirect("core:index")
        else:
        	return redirect("core:cart")

    def get(self, request):
        return HttpResponseRedirect(f"products/{request.get_full_path()[1:]}")


def user_logout(request):
    logout(request)
    return redirect("core:home")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        return render(
            request, "index.html", {"categories": categories, "products": products}
        )


class ProductView(View):

    def get(self, request):
        data = {}
        cart = request.session.get("cart")
        if not cart:
            request.session["cart"] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get("category")
        if categoryID:
            products = Product.objects.filter(category=categoryID)
        else:
            products = Product.objects.all()

        data["products"] = products
        data["categories"] = categories

        return render(request, "index.html", data)


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.data["password"])
            user.save()
            messages.success(request, "User Registered Successfully")
            return redirect("core:login")
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect("/signup/")
        return render(request, "signup.html", {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # message = f'Hello {user.username}! You have been logged in'
                return redirect("core:home")
            else:
                message = "Please provide valid username and password"
                messages.error(request, message)
                return redirect("core:login")
        else:
            messages.error(request, form.errors)
            return redirect("core:login")


class CartView(View):
    def get(self, request):
        products = None
        user = request.user
        cart = request.session.get("cart")
        if cart:
            ids = list(cart.keys())
            products = Product.get_products_by_id(ids)
        return render(request, "cart.html", {"products": products,'user':user})


class CheckOut(View):
    def post(self, request):
        address_type = request.POST.get('add')
        if address_type == "1":
        	address = request.user.address
        	phone = request.user.mobile_number
        else:
	        address = request.POST.get("address")
	        phone = request.POST.get("phone")
        cart = request.session.get("cart")
        products = Product.objects.filter(id__in=cart.keys())
        order = Order.objects.create(
            customer=request.user,
            address=address,
            phone=phone,
            status="Panding",
            date=today,
        )
        total_amount = total_cart_price(products,cart)
        for product in products:
            order_product = OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=cart.get(str(product.id)),
                price=product.price,
                total_amount=total_amount,
            )
        # request.session['cart'] = {}
        return redirect("core:payment")


class PaymentView(View):

    def get(self, request):
        order = None
        cart = request.session.get("cart")
        client_id = settings.PAYPAL_CLIENT_ID
        coupon = Coupon.objects.filter(user=request.user,valid_from__lte=timezone.now(), valid_to__gte=timezone.now()).last()
        products = Product.objects.filter(id__in=cart.keys())
        order = Order.objects.filter(customer=request.user).last()
        order_product = OrderProduct.objects.filter(
            product__in=products, order=order
        ).last()
        if order_product:
            order = order_product.order
        if coupon:
        	final_amount = order_product.total_amount - coupon.amount
        return render(
            request,
            "checkout.html",
            {"products": products,
            "client_id": client_id,
            "order": order,
            "coupon":coupon,
            "order_product":order_product,
            "final_amount":final_amount},
        )

    def post(self, request):
        code = request.POST.get('code')
        if code:
            order = Order.objects.filter(customer=request.user).last()
            coupon = Coupon.objects.filter(code__iexact=code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now()).exclude(user=request.user,max_value__lte=F('used')).first()
            if not coupon:
                messages.error(self.request, 'You can\'t use same coupon again, or coupon does not exist')
                return redirect('core:payment')
            else:
                try:
                    order_product = OrderProduct.objects.filter(order=order)
                    total_amount = order_product[0].total_amount - coupon.amount
                    for itm in order_product:
                    	itm.coupon = coupon
                    	itm.total_amount = total_amount
                    	itm.save()
                    coupon.used += 1
                    coupon.save()
                    order.apply_coupon = True
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                except:
                    messages.error(self.request, "Max level exceeded for coupon")
        
                return redirect('core:payment')
        else:
            my_json = request.body.decode("utf8").replace("'", '"')
            user = request.user
            order_mail = order_confirmation_mail(my_json,user)
            request.session["cart"] = {}
            return JsonResponse({"success": True, "url": "/payment/done/"})



class PaymentDoneView(View):

    def get(self, request):
        order = Order.objects.filter(customer=request.user).last()
        order_delivery_date = order.date + datetime.timedelta(days=7)
        return render(
            request,
            "payment_done.html",
            {"order": order, "order_delivery_date": order_delivery_date},
        )



class OrderHistoryView(View):

    def get(self, request):
        all_order_product = []
        orders = Order.objects.filter(customer=request.user)
        for order in orders:
        	order_products = OrderProduct.objects.filter(order=order)
        	if order_products:
	        	for or_product in order_products:
	        		all_order_product.append(or_product)
        return render(
            request,
            "order_history.html",
            {"all_order_product": all_order_product,},
        )
