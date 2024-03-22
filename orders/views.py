from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If cart count is less then or equal to 0, then redirect user to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Store all the billing information inside Order table
            # Create Order instance 
            data = Order()
            
            data.first_name = form.cleaned_data('first_name')
            data.last_name = form.cleaned_data('last_name')
            data.email = form.cleaned_data('email')
            data.phone_number = form.cleaned_data('phone_number')
            data.address_line_1 = form.cleaned_data('address_line_1')
            data.address_line_2 = form.cleaned_data('address_line_2')
            data.city = form.cleaned_data('city')
            data.state = form.cleaned_data('state')
            data.country = form.cleaned_data('country')
            data.order_note = form.cleaned_data('order_note')
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d') #20240322
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
    else:
        return redirect('checkout')    