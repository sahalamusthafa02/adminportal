from django.db.models import fields
from rest_framework import serializers
from .models import Customer , Invoice
from .models import Customer, Invoice

class  CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone','email','address']

class  InvoiceSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer() 
    class Meta:
        model=Invoice
        fields='__all__'