from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContactForm
        fields = ['name', 'phone', 'email', 'place', 'id']
class CustomerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContactForm
        fields = ['name', 'phone', 'email', 'place']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeContactForm
        fields = ['name', 'phone', 'email', 'place', 'salary', 'id']

class EmployeePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeContactForm
        fields = ['name', 'phone', 'email', 'place', 'salary']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryFormData
        fields = ['name', 'id']

class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryFormData
        fields = ['name']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorContactForm
        fields = ['name', 'phone', 'email','id']

class VendorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorContactForm
        fields = ['name', 'phone', 'email']

class ProductSerializer(serializers.ModelSerializer):
    product = CategorySerializer()
    class Meta:
        model = productFormData
        fields = ['name','price', 'product', 'id']

class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = productFormData
        fields = ['name','price', 'product']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseFormData
        fields = ['vendor', 'product', 'bill', 'buy', 'type', 'quantity', 'sell', 'id']

class PurchasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseFormData
        fields = ['vendor', 'product', 'bill', 'buy', 'type', 'quantity', 'sell']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['product', 'total_quantity', 'selling_price', 'id']

class StockPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['product', 'total_quantity', 'selling_price']

class SalesSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source='customer.name', read_only=True)
    employeeName = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = SalesForm
        fields = ['id', 'customer', 'employee', 'customerName', 'employeeName', 'total_amount', 'type']

class SalesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = ['customer', 'employee', 'total_amount', 'type']

class SaleItemSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source='stock.product.name', read_only=True)
    customerName = serializers.CharField(source='sales_form.customer.name', read_only=True)
    employeeName = serializers.CharField(source='sales_form.employee.name', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'sales_form', 'stock', 'quantity', 'productName', 'customerName', 'employeeName']

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
        fields = ['expense', 'amount','id']
class ExpensePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = expenseData
        fields = ['expense', 'amount']