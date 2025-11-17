from dataclasses import field
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput
from django import forms


# For login 
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# update username or email
class UpdateUserForm(forms.ModelForm):

    password = None

    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self,  *args, **kwargs):
        # super(CreateUserForm, self).__init__(*args, **kwargs)   
        super(UpdateUserForm,self).__init__(*args, **kwargs)   # calling the constructer of UserCreationForm

        self.fields['email'].required= True


    # Email validation
    def clean_email(self):
        # clean_data is the feature of form class after validation the data is stored in the clean_data dictionary
        email = self.cleaned_data.get('email')

        # chceking email is existed already
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('This email is invalid')
        
        if len(email) >= 350:
                
            raise forms.ValidationError('Your email is invalid')
        
        # to save the email in database
        return  email



# for Registration
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self,  *args, **kwargs):
        # super(CreateUserForm, self).__init__(*args, **kwargs)   
        super().__init__(*args, **kwargs)   # calling the constructer of UserCreationForm

        self.fields['email'].required= True



    # django have inbuild username validation (user-verification in build)
    # checkiing email must be unique
    def clean_email(self):
        # clean_data is the feature of form class after validation the data is stored in the clean_data dictionary
        email = self.cleaned_data.get('email')

        # chceking email is existed already 
        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('This email is invalid')
        
        if len(email) >= 350:
            
            raise forms.ValidationError('Your email is invalid')
        
        # to save the email in database
        return  email












