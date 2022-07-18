from .models import Category, Product, Order, OrderProduct
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.loader import get_template



def order_confirmation_mail(my_json,user):
    data_list = my_json.split("&")
    PaypalorderID = data_list[0].split("=")[1]
    status = data_list[1].split("=")[1]
    transactionID = data_list[2].split("=")[1]
    order_id = data_list[3].split("=")[1]
    order = Order.objects.filter(id=order_id, customer=user).last()
    if status == 'COMPLETED':
        order.status = 'Processing'
    else:
        order.status = 'Panding'
    order.transaction_id = transactionID
    order.save()
    order_product = OrderProduct.objects.filter(order=order)
    ctx = {'order': order,'order_product':order_product}
    message = get_template('mail.html').render(ctx)
    customer_email = order.customer.email
    subject = "YOUR ORDER"
    html_body = message
    from_email='admin@example.com'
    body = message
    to=[customer_email,'yashdeep.tiwari@neosoftmail.com']


    message = EmailMultiAlternatives(subject, body, from_email, to)
    message.attach_alternative(html_body, "text/html")
    # message.send()
