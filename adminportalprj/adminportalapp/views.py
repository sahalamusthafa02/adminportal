from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User
from adminportalapp.models import Customer, Invoice
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer , InvoiceSerializer
from rest_framework import status
# Create your views here.

def index(request):
    return render(request, 'index.html')

def customer(request):
    customers = Customer.objects.all()
    return render(request,'customer.html',{'customers':customers})

def invoice(request):
    invoices = Invoice.objects.all()
    return render(request,'invoice.html',{'invoices':invoices})

def createnewCus(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']

        customer = Customer(name=name, phone=phone, email=email, address=address)
        customer.save()

        return redirect('customer')
    else:
        customers = Customer.objects.all()
        return render(request, 'createnewCus.html', {'customers': customers})

def createnewInv(request):
    if request.method == 'POST':
        customer_id = request.POST['customer']
        date = request.POST['date']
        amount = request.POST['amount']
        status = request.POST['status']

        customer = Customer.objects.get(id=customer_id)
        invoice = Invoice(customer=customer, date=date, amount=amount, status=status)
        invoice.save()
        return redirect('invoice')
    else:
        cust = Customer.objects.all()
        return render(request, 'createnewInv.html', {'customer': cust})

def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.name = request.POST['name']
        customer.phone = request.POST['phone']
        customer.email = request.POST['email']
        customer.address = request.POST['address']
        customer.save()
        messages.success(request, 'customer updated successfully.')
        return redirect('customer')
    else:
        return render(request, 'updateCus.html', {'customer': customer})

def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        customer_id = request.POST['customer']
        date = request.POST['date']
        amount = request.POST['amount']
        status = request.POST['status']

        customer = Customer.objects.get(id=customer_id)
        invoice.customer = customer
        invoice.date = date
        invoice.amount = amount
        invoice.status = status
        invoice.save()
        messages.success(request, 'Invoice updated successfully.')
        return redirect('invoice')
    else:
        cust = Customer.objects.all()
        return render(request, 'updateinv.html', {'invoice': invoice, 'cust': cust})

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if password != confirmPassword:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        myuser = User.objects.create_user(username,email, password)
        myuser.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')

def logout(request):
    return render (request,'logout.html')



@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_customer': '/all',
        'Search by Name': '/?name=name_name',
        'Search by Phone': '/?phone=name_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/customer/pk/delete',
        'all_invoice': '/invoices',
        'add_invoice': '/invoices/create',
        'update_invoice': '/invoices/update/pk',
        'delete_invoice': '/invoices/pk/delete'
    }
    return Response(api_urls)

@api_view(['POST'])
def add_customers(request):
    Customers = CustomerSerializer(data=request.data)
 
    # validating for already existing data
    if Customer.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if Customers.is_valid():
        Customers.save()
        return Response(Customers.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_customers(request):
     
    if request.query_params:
        customers = Customer.objects.filter(**request.query_params.dict())
    else:
        customers = Customer.objects.all()
 
    if customers:
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_customers(request, pk):
    customer = Customer.objects.get(pk=pk)
    data = CustomerSerializer(instance=customer, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_customers(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def add_invoices(request):
    Invoices = InvoiceSerializer(data=request.data)
 
    # validating for already existing data
    if Invoice.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if Invoices.is_valid():
        Invoices.save()
        return Response(Invoices.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_invoices(request):
     
    if request.query_params:
        invoices = Invoice.objects.filter(**request.query_params.dict())
    else:
        invoices = Invoice.objects.all()
 
    if invoices:
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_invoices(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    data = InvoiceSerializer(instance=invoice, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_invoices(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
