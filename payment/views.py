from statistics import quantiles
from django.shortcuts import render

from .models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.http import JsonResponse
from decimal import Decimal

# Create your views here.


def payment_success(request):

  # if payment is successful then we wnat to clear the cart
  # to do that we del session key 
  for key in list(request.session.keys()):
    
    if key == 'session_key':
      del request.session[key]

  return render(request, 'payment/payment-success.html')


def payment_failed(request):

  return render(request, 'payment/payment-fail.html')



def checkout(request):
  
  # if user have account - pre-filled shipping address
  if request.user.is_authenticated:
    # check user have shipping address or not
    try:
      shipping_address = ShippingAddress.objects.get(user=request.user.id)
      # print(shipping_address)

      context = {'shipping': shipping_address}
    
      return render(request, 'payment/checkout.html', context=context)
    
    except:
      # user is authenticated but no shippng address
      return render(request, 'payment/checkout.html')
    
  # Guest User

  return render(request, 'payment/checkout.html')


def complete_checkout(request):
  
  if request.POST.get('action') == 'post':

    name = request.POST.get('name')
    email = request.POST.get('email')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address1')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zipcode = request.POST.get('zipcode')


    # style user All - in - one shipping address
    shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n'  + zipcode)


    # using cart functionality
    cart = Cart(request)

    total_cost = cart.get_total()


    '''
    1) if user is autheticated

    2) Guest User
    
    '''
    if request.user.is_authenticated:
      # so we have user id
      order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)

      # create OrderItem object 
      # need order id and product id b/c those are foreign key in our model

      # using this way we can easily relate the product and the ordes
      for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user)

    else:
    # create order for guest user
        order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)

        # create OrderItem object 
        # need order id and product id b/c those are foreign key in our model

        # using this way we can easily relate the product and the ordes
        for item in cart:
          OrderItem.objects.create(order=order, product=item['product'], quantity=item['qty'], price=item['price'])


  order_success = True

  response = JsonResponse({'success': order_success})

  return response



