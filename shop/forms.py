from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import Order
 
class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
  email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']
    
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'state', 'pincode', 'order_notes']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'House No., Street, Landmark',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '6-digit PIN code'
            }),
            'order_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special instructions? (Optional)',
                'rows': 2
            }),
        }
