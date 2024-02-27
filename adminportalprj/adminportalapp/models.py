from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.name}"