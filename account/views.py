from email import message
import pstats
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from .form import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth.models import User

from payment.models import Order, OrderItem


# this is used to get domain and name of current site based on site_id or host
from django.contrib.sites.shortcuts import get_current_site

# calling variable of token.py
from .token import user_tokenizer_generate


# function is used to render a Django template using the provided context and returns the rendered HTML as a string.
from django.template.loader import render_to_string

# These functions are used for encoding and decoding strings to and from bytes
from django.utils.encoding import force_bytes, force_str

# decode and encode the token we are sending
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# required for authentication
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# messagin 
from django.contrib import messages

# import payment form
from payment.forms import ShippingForm
from payment.models import ShippingAddress


# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':

        # retriving all the data submit by the user
        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            # ovr-riding obj  --> making obj inactive
            user.is_active = False

            user.save()
            
            # email verification  setup( a tmplate to email-verification-setup)

            # get the domain and name of site 
            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'user_id': urlsafe_base64_encode(force_bytes(user.pk)), # encoding userid
                'token': user_tokenizer_generate.make_token(user)

            })

            
            user.email_user(subject=subject, message=message, fail_silently=False)


            return redirect('email-verification-sent')

            
    # creating a dict to store form data and pass this to register.html
    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)


# verifying the email
def email_verification(request, uidb64, token):

    # decoding the userid
    
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    

    if user and user_tokenizer_generate.check_token(user, token):
        
        # make user active
        user.is_active = True
        user.save()

        return redirect('email-verification-success')
    
    else:

        return redirect('email-verification-failed')
    
    

def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')



def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')



def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')



def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)

            return redirect('dashboard')
        
    context = {'form': form}

    return render(request, 'account/login.html', context=context)



def user_logout(request):
    # How to save that data on a user's local machine (e.g., using cookies, local storage, or other browser storage),
    # auth.logout(request)  

    try:
        for key in list(request.session.keys()):

            if key == "session_key":
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    
    # b/x we are redirecting  to store page we add this fucntionality in the base.html
    messages.success(request, "LogOut successfully!")

    return redirect('store')


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login')
def profile_manage(request):

    user_form = UpdateUserForm(instance=request.user)
    
    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Account updated!")
            return redirect('dashboard')
        

    # user information generated automatially


    context = {'user_form': user_form}

    return render(request, "account/profile-management.html", context=context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()

        messages.error(request, "Account deleted successfully!")
        redirect('store')

    return render(request, "account/delete-account.html")

# shipping view
@login_required(login_url='my-login')
def manage_shipping(request):
    
    try:
        # if user have shipping address
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:
        shipping = None

    # if user have shippping data then we user old obj otherwise we create a new one
    form = ShippingForm(instance=shipping)

    if request.method == 'POST':

        # when some one post the shipping form data we update the data of shipping object not cerate a new one
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():

            # assigning foreign kye to the object
            shipping_user = form.save(commit=False)  # created a intance of the form 

            shipping_user.user = request.user  # assigmin the Fk

            shipping_user.save()

            return redirect('dashboard')
        

    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_order(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)

        context = {'orders' : orders}

    
        return render(request, 'account/track-order.html', context=context)

    except:
        return render(request, 'account/track-order.html')


   











