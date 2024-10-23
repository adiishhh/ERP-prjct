from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContactForm
        fields = ['name', 'phone', 'email', 'place']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeContactForm
        fields = ['name', 'phone', 'email', 'place', 'salary']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryFormData
        fields = ['name']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorContactForm
        fields = ['name', 'phone', 'email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = productFormData
        fields = ['name', 'unit', 'price', 'product']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseFormData
        fields = ['vendor', 'product', 'bill', 'buy', 'type', 'quantity', 'sell']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['product', 'total_quantity', 'selling_price']

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = ['customer', 'employee', 'total_amount', 'type']

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['id', 'sales_form', 'stock', 'quantity', 'type']

class SalesFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = ['id', 'type', 'total_amount']

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['id', 'total_quantity', 'selling_price']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['debit', 'credit', 'type']  

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountData
        fields = ['debit', 'credit', 'type'] 

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = expenseData
        fields = ['expense', 'amount']