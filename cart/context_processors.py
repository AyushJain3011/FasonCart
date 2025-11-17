from .cart import Cart


# this function will return all the functionality and feature of cart which will be accessed by every page in our site
# add this ot ecommerce/setting.py in context_processor
def cart (request):

    return {'cart' : Cart(request)}






