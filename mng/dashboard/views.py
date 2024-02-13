
from django.shortcuts import render,redirect
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView
from .models import Product
from .forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib import auth
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import  AuthenticationForm



@login_required
def index(request):
    return render(request, 'dashboard/index.html')
@login_required
def page_add_cat(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your category has been added!')
            return redirect('page_add_cat')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/page_add_cat.html', {'form': form})
@login_required
def page_add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase added successfully!')
            return redirect('page_add_purchase')
    else:
        form = PurchaseForm()
    return render(request, 'dashboard/page_add_purchase.html', {'form': form})

@login_required
def page_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your product has been added!')
            return redirect('page_add_product')
    else:
        form = ProductForm()
        
    return render(request, 'dashboard/page_add_product.html', {'form': form})

@login_required
def page_add_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale_form.save()
            messages.success(request, 'Sale added successfully!')
            return redirect('page_add_sale')
    else:
        sale_form = SaleForm()
    return render(request, 'dashboard/page_add_sale.html', {'sale_form': sale_form})
@login_required
def page_list_cat(request):
    pages=Category.objects.all()
    context={
        'pages':pages
    }
    return render(request, 'dashboard/page_list_cat.html', context)
@login_required
def page_list_product(request):
    pages=Product.objects.all()
    context={
        'pages':pages
    }
    return render(request, 'dashboard/page_list_product.html', context)
@login_required
def page_list_sale(request,id):
    pages=Sale.objects.all()
    cust=Customer.objects.get(id=id)
    context={'pages':pages,'cust':cust}
    
    return render(request,'dashboard/page_list_sale.html',context)
@login_required
def page_list_purchase(request):
    pages=Purchase.objects.all()
    context={
        'pages':pages
    }
    return render(request, 'dashboard/page_list_purchase.html', context)
    
@login_required   
def page_add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase added successfully!')
            return redirect('page_add_purchase')
    else:
        form = PurchaseForm()
    return render(request, 'dashboard/page_add_purchase.html', {'form': form})

@login_required
def page_list_purchase(request):
    pages=Purchase.objects.all()
    context={
        'pages':pages
    }
    return render(request, 'dashboard/page_list_purchase.html', context)
    
@login_required  
def page_add_customers(request):
    if request.method == 'POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('page_add_customers')
    else:
        form=CustomerForm()
    return render(request,"people/page_add_customers.html",{'form':form}) 
@login_required
def page_list_customers(request):
    customers=Customer.objects.all().order_by("name")
    paginator = Paginator(customers, 10) # Show  25 contacts per page.
    page = request.GET.get('page')      
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:    
        customers = paginator.page(1)
    except EmptyPage:                
        customers = paginator.page(paginator.num_pages)          
    context={'customers':customers}
    return render(request,'people/page_list_customers.html',context)
@login_required   
def page_add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')  # Get the email from the form data
            if Supplier.objects.filter(email=email).exists():  # Check if supplier with this email already exists
                messages.error(request, 'Supplier with this email already exists!')
            else:
                form.save()
                messages.error(request, 'Supplier added successfully!')
                return redirect('page_add_supplier')
    else:
        form = SupplierForm()
    return render(request, "people/page_add_supplier.html", {'form': form}) 

# @staff_member_required
@login_required
def page_list_supplier(request):
    suppliers = Supplier.objects.all().order_by("name")
    paginator = Paginator(suppliers, 10)  # Show 10 suppliers per page
    page = request.GET.get('page')
    try:
        suppliers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        suppliers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        suppliers = paginator.page(paginator.num_pages)
    context = {"suppliers": suppliers}
    return render(request, "people/page_list_supplier.html", context)

@login_required

def page_add_return(request):
    """Add a new Return to the database."""
    if request.user.has_perm('sales.add_return'):
        form = ReturnForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Return added successfully!')
            return HttpResponseRedirect('/page_add_return/')
    else:
        form=ReturnForm()
    return render(request, 'dashboard/page_add_return.html', {'form': form})

@login_required

def page_add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            if not hasattr(user, 'profile'):
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('page_add_user')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'user/page_add_user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')  # Replace 'home' with the name of your home URL pattern
        else:
            # Return an 'invalid login' error message.
            return render(request, 'user/auth_login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'user/auth_login.html')
