from django.shortcuts import render
from .models import Customer, Product, Cart, OrderPlaced
from django.views import View
from .form import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomswears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        # laptop = Product.object.filter(category = 'L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomswears, 'mobiles': mobiles})


# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    return render(request, 'app/addtocart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


def orders(request):
    return render(request, 'app/orders.html')


def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000.0)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self, request):
        messages.warning(request, 'Enter the Data below below.')
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulation Registered Successfully ')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            n = form.cleaned_data['name']
            l = form.cleaned_data['locality']
            c = form.cleaned_data['city']
            z = form.cleaned_data['zipcode']
            s = form.cleaned_data['state']
            reg = Customer(user=usr, name=n, locality=l,
                           city=c, zipcode=z, state=s)
            reg.save()
            messages.success(
                request, 'congratualtion profile Updeted successfully')

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
