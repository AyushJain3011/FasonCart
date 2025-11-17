from django.shortcuts import render, HttpResponse
from . cart import Cart
from store.models import Product
from django.shortcuts import get_list_or_404
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    cart = Cart(request)

    return render(request, 'cart/cart-summary.html', context={'cart':cart})
    

def cart_add(request):
    """
    1) check the req type 
    2) get the data from front end using AJAX
    3) call the fuction to update the view of cart
    """
    #create a obj of cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
       
        # we get the product id then we can get the product ID from our model
        product = get_list_or_404(Product, id=product_id)[0]   # ---> List
        
        # call the function of cart class ot add product
        cart.add(product=product, product_qty = product_quantity)

        # formating response in json format --> json format work in dictionary format
        cart_qty = cart.__len__()  # for curr qty of the products
        response = JsonResponse({'qty': cart_qty})

        return response
       

def cart_delete (request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        cart_qty = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_qty, 'cart_total': cart_total})

        return response



def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))


        cart.update(product=product_id, product_qty=product_qty)

        cart_qty = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_qty, 'cart_total': cart_total})

        return response