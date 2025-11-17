

"""
This is the file where we define all the functionality of our cart
It stores data on the server side and abstracts the sending and receiving of cookies(contain session ID)
"""

from store.models import Product
from decimal import Decimal


class Cart:

    def __init__(self, request):

        self.session = request.session  #getting session Id in dict format

        
        # returning user: his/her session key
        cart = self.session.get('session_key')

        # generating a new session key for the new user
        if 'session_key' not in request.session:
            
            # assigning user a session key
            cart = self.session['session_key'] = {}


        # return user have product in the cart or not 
        self.cart = cart


    # this function is used to add product and prodict_qty in 
    def add(self, product, product_qty):
        # reason for changing it into string b/c we does not want any operation on product
        product_id = str(product.id)  

        # if product_id is in cart
        if product_id in self.cart:
            self.cart[product_id]['qty'] += product_qty

        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        
        # boolean attribute signal that data has been changed and need to be saved
        self.session.modified = True
        # print(self.cart)


    # this function will return the number of item in our shopping-cart
    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())
    

    # creating a list on which we can iterate and present in our car-summary.html
    def __iter__(self):

        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        import copy

        cart = copy.deepcopy(self.cart)

        for product in products:
            # full product object
            cart[str(product.id)]['product'] = product

        
        # calc price  {'3': {'price': '30.00', 'qty': 1, 'product': product, 'total' = }}
        for item in cart.values():
            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']

            yield item

    def get_total(self):
      
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())


    def delete(self, product):
        
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


    def update(self, product, product_qty):
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty     

        self.session.modified = True






            





















