from django import forms
from .models import*
from django.contrib.auth.forms import UserCreationForm  

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False 
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image'):
            instance.image = self.cleaned_data.get('image')
            instance.save()
        if commit:
            instance.save()
        return instance
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields='__all__'
        widgets={
            'type': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
            'category': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
            'tax_method': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
        }
        labels = {'price':'Price (RM)'}
        help_texts = {'description':"Please enter a brief description of the product."}
    
        
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        widgets ={
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_tax': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
            'biller': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
            'sale_status': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
            'payment_status': forms.Select(attrs={'class': 'selectpicker form-control', 'data-style': 'py-0'}),
        }
        exclude = ['created_at']
        
class SupplierForm(forms.Form):
    class Meta:
        model = Supplier
        fields = '__all__'
    
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
    def save(self):
        instance = super().save(commit=False)
        instance.supplier = Supplier.objects.get(id=self.cleaned)
        return instance
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        
class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = '__all__'
        widgets={
            'biller': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'order_tax': forms.Select(attrs={'class': 'form-control'}),
            
        }
        
        

    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone_number', 'gender','status','notify_by_email']