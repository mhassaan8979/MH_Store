from django.shortcuts import render, redirect
from .models import Product, Customer, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def home(request):
 total_items = 0
 mobile = Product.objects.filter(category='M')
 laptop = Product.objects.filter(category='L')
 topwear = Product.objects.filter(category='TW')
 bottomwear = Product.objects.filter(category='BW')
 if request.user.is_authenticated:
  total_items = len(Cart.objects.filter(user=request.user))
 context = {
  'mobile': mobile,
  'laptop': laptop,
  'topwear': topwear,
  'bottomwear': bottomwear,
  'total_items':total_items
 }
 return render(request, 'main/home.html', context)


def product_detail(request, pk):
 p = Product.objects.get(pk=pk)
 item_already_in_cart = False
 if request.user.is_authenticated:
  item_already_in_cart = Cart.objects.filter(Q(product=p.id) & Q(user=request.user)).exists()
 context = {
  'p': p,
  'item_already_in_cart':item_already_in_cart,
 }
 return render(request, 'main/productdetail.html', context)


def mobile(request, data=None):
 if data == None:
  mobile = Product.objects.filter(category='M')
 elif data == 'Apple' or data == 'Samsung' or data == 'OnePlus':
  mobile = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'Below':
  mobile = Product.objects.filter(category='M').filter(discounted_price__lt=100000)
 elif data == 'Above':
  mobile = Product.objects.filter(category='M').filter(discounted_price__gt=100000)
 context = {
  'mobile': mobile,
 }
 return render(request, 'main/mobile.html', context)


def laptop(request, data=None):
 if data == None:
  laptop = Product.objects.filter(category='L')
 elif data == 'Apple' or data == 'Samsung' or data == 'Dell' or data == 'HP':
  laptop = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'Below':
  laptop = Product.objects.filter(category='L').filter(discounted_price__lt=100000)
 elif data == 'Above':
  laptop = Product.objects.filter(category='L').filter(discounted_price__gt=100000)
 context = {
  'laptop': laptop,
 }
 return render(request, 'main/laptop.html', context)


def top_wear(request, data=None):
 if data == None:
  top_wear = Product.objects.filter(category='TW')
 elif data == 'Saint' or data == 'Polo' or data == 'Apricot' or data == 'Nike' or data == 'Crux' or data == 'Grande':
  top_wear = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'Below':
  top_wear = Product.objects.filter(category='TW').filter(discounted_price__lt=1200)
 elif data == 'Above':
  top_wear = Product.objects.filter(category='TW').filter(discounted_price__gt=1200)
 context = {
  'top_wear': top_wear,
 }
 return render(request, 'main/top_wear.html', context)


def bottom_wear(request, data=None):
 if data == None:
  bottom_wear = Product.objects.filter(category='BW')
 elif data == 'Jack-Jones' or data == 'Polo' or data == 'Huesen' or data == 'Calvin' or data == 'Crux' or data == 'OuterKnown' or data == 'Lager':
  bottom_wear = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'Below':
  bottom_wear = Product.objects.filter(category='BW').filter(discounted_price__lt=2000)
 elif data == 'Above':
  bottom_wear = Product.objects.filter(category='BW').filter(discounted_price__gt=2000)
 context = {
  'bottom_wear': bottom_wear,
 }
 return render(request, 'main/bottom_wear.html', context)


def search(request):
 query = request.GET.get('query')
 product = Product.objects.filter(title__icontains=query)
 context = {
  'product': product
 }
 return render(request, 'main/search.html', context)


def customerregistration(request):
 if request.method == "GET":
  form = CustomerRegistrationForm()
  return render(request, 'main/customerregistration.html', {'form':form})
 elif request.method == "POST":
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'main/customerregistration.html', {'form':form})
 

@login_required
def profile(request):
 if request.method == "GET":
  form = CustomerProfileForm()
  return render(request, 'main/profile.html', {'form':form, 'active':'btn-primary'})
 elif request.method == "POST":
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name =form.cleaned_data['name']
   locality =form.cleaned_data['locality']
   city =form.cleaned_data['city']
   zipcode =form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request, 'main/profile.html', {'form':form, 'active':'btn-primary'})


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'main/address.html', {'add':add, 'active':'btn-primary'})


@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 crt = Cart(user=user, product=product)
 crt.save()
 return redirect('show_cart')


@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount = 70.0
  total_amount= 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount
    total_amount = amount + shipping_amount
   return render(request, 'main/add_to_cart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
  else:
   return render(request, 'main/empty_cart.html')



def plus_cart(request):
 if request.method =='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity += 1
    c.save()
    amount= 0.0
    shipping_amount = 70.0
    total_amount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      temp_amount = (p.quantity * p.product.discounted_price)
      amount += temp_amount
    
    data = {
    'quantity': c.quantity,
    'amount': amount,
    'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)
 

def minus_cart(request):
  if request.method =='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()
    amount= 0.0
    shipping_amount = 70.0
    total_amount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      temp_amount = (p.quantity * p.product.discounted_price)
      amount += temp_amount
    
    data = {
    'quantity': c.quantity,
    'amount': amount,
    'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)
  

def remove_cart(request):
  if request.method =='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount= 0.0
    shipping_amount = 70.0
    total_amount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      temp_amount = (p.quantity * p.product.discounted_price)
      amount += temp_amount

    data = {
    'amount': amount,
    'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)


@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount = 70.0
  total_amount= 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
    for p in cart_product:
      temp_amount = (p.quantity * p.product.discounted_price)
      amount += temp_amount
    total_amount = amount + shipping_amount
    return render(request, 'main/checkout.html', {'cart_items':cart_items,'total_amount':total_amount, 'add':add})
  

@login_required
def payment_done(request):
 user = request.user
 cstid = request.GET.get('cstid')
 customer = Customer.objects.get(id=cstid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect('orders')


@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'main/orders.html', {'order_placed':op})


def buy_now(request):
 return render(request, 'main/buynow.html')
