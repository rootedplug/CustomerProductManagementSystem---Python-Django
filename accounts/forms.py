from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Orders 
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']