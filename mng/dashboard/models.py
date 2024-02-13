from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save





class Customer(models.Model):    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    customer_group = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
class Category(models.Model): 
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/',default=None)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):   
    TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('combo', 'Combo'),
        ('digital', 'Digital'),
        ('service', 'Service'),
    ]

    TAX_CHOICES = [
        ('exclusive', 'Exclusive'),
        ('inclusive', 'Inclusive'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    barcode_symbology = models.CharField(max_length=10)
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_method = models.CharField(max_length=10, choices=TAX_CHOICES)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/',default=None)
    description = models.TextField()

    def __str__(self):
        return self.name
    




class Sale(models.Model):
    

    BILLER_CHOICES = [
        ('Test Biller', 'Test Biller'),
        # Add other biller choices here if needed
    ]

    ORDER_TAX_CHOICES = [
        ('No Text', 'No Text'),
        ('GST @5%', 'GST @5%'),
        ('VAT @10%', 'VAT @10%'),
    ]

    SALE_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Due', 'Due'),
        ('Paid', 'Paid'),
    ]

    reference_no = models.CharField(max_length=50, null=False, blank=False)
    biller = models.CharField(max_length=50, choices=BILLER_CHOICES, null=False, blank=False)
    customer = models.ManyToManyField(Customer)
    order_tax = models.CharField(max_length=50, choices=ORDER_TAX_CHOICES, null=True, blank=True)
    order_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    attach_document = models.FileField(upload_to='sales/documents/', null=True, blank=True)
    sale_status = models.CharField(max_length=50, choices=SALE_STATUS_CHOICES, null=False, blank=False)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, null=False, blank=False)
    sale_note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reference_no 
    
    


class Supplier(models.Model):   
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=15)
    address = models.TextField()  
    company_Name=models.CharField(max_length=225)
    city = models.CharField(max_length=255, )  # Provide a default value for city
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
        

class Purchase(models.Model):
    purchase_no = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)
    order_tax = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purchase_no

    def save(self, *args, **kwargs):
        self.total_amount = self.payment - self.discount + self.shipping
        super(Purchase, self).save(*args, **kwargs)



    
class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    details = models.ManyToManyField(Product, through='OrderDetails')
    is_finished=models.BooleanField()
    def __str__(self):
     return f"{self.customer.name} - {self.order_date}"
class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    
    
    
    
    
    
    

class Return(models.Model):
    reference_no = models.CharField(max_length=50, unique=True)
    biller = models.CharField(max_length=50, choices=[(tag, tag) for tag in ['Test Biller']])
    customer =models.ForeignKey(Customer,null=True, blank=True, on_delete=models.CASCADE)
    order_tax = models.CharField(max_length=50, choices=[(tag, tag) for tag in ['No Text', 'GST @5%', 'VAT @10%']])
    order_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shipping = models.DecimalField(max_digits=5, decimal_places=2)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    return_note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.reference_no








class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True, blank=True, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField('email Address', unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')))
    status = models.CharField(max_length=10, choices=(('Active', 'Active'), ('Inactive', 'Inactive')))
    notify_by_email = models.BooleanField(default=True)

   
    
    def __str__ (self):
        return self.user.username
    
    
   



