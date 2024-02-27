from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('invoice/', views.invoice, name='invoice'),
    path("invoice/<int:pk>/update/", views.update_invoice, name="update_invoice"),
    path('customer/new/', views.createnewCus, name='createnewCus'),
    path('customer/<int:pk>/update/', views.update_customer, name='update_customer'),
    path('invoice/new/', views.createnewInv, name='createnewInv'),
    path('login/signup/', views.login1, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('createcustomer/', views.add_customers, name='add-customers'),
    path('allcustomer/', views.view_customers, name='view_customers'),
    path('updatecustomer/<int:pk>/', views.update_customers, name='update-customers'),
    path('customer/<int:pk>/delete/', views.delete_customers, name='delete-customers'),
    path('createinvoice/', views.add_invoices, name='add-invoices'),
    path('allinvoice/', views.view_invoices, name='view_invoices'),
    path('updateinvoice/<int:pk>/', views.update_invoices, name='update-invoices'),
    path('invoice/<int:pk>/delete/', views.delete_invoices, name='delete-Invoices'),

    path('apioverview/',views.ApiOverview,name='apioverview')
]