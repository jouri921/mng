from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('page_add_product/',page_add_product,name='page_add_product'),
    path('page_list_product/',page_list_product,name='page_list_product'),
    path('page_add_cat/',page_add_cat,name='page_add_cat'),
    path('page_list_cat/',page_list_cat,name='page_list_cat'),
    path('page_add_sale/', page_add_sale, name="page_add_sale"),
    path('page_list_sale/', page_list_sale, name="page_list_sale"),
    path('page_add_purchase/',page_add_purchase,name="page_add_purchase"),
    path('page_list_purchase/',page_list_purchase,name="page_list_purchase"),
    
    path('page_add_customers/',page_add_customers,name="page_add_customers"),
    path('page_list_customers/',page_list_customers,name="page_list_customers"),
    path('page_add_supplier/',page_add_supplier,name="page_add_supplier"),
    path('page_list_supplier/',page_list_supplier,name="page_list_supplier"),
    path('page_add_return/',page_add_return,name="page_add_return"),
    #path('page_list_return/',page_list_return,{'type':'retornos'},name="page_list_return"),  
   # path('page_list_return/',page_list_return,name="page_list_return"), 
    path('page_add_user/',page_add_user,name="page_add_user"),
]