from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, StaffProfile, Ingredient, Order

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Password'}))

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password1', 'password2')

class StaffProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}), required=False)

    class Meta:
        model = StaffProfile
        fields = ('shift', 'phone', 'address')
        widgets = {
            'shift': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'address': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 2}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'unit', 'current_stock', 'low_stock_threshold')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'unit': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white stock-input', 'step': '0.01'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white', 'step': '0.01'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('table_number', 'order_type')
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'order_type': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }