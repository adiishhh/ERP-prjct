from django.db import models

# Create your models here.

class CustomerContactForm(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    place = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class employeeContactForm(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    place = models.CharField(max_length=200)
    salary = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class categoryFormData(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class vendorContactForm(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name
    
class productFormData(models.Model):
    product = models.ForeignKey(categoryFormData, on_delete=models.CASCADE)
    name = models.TextField(max_length=200)
    unit = models.TextField(max_length=200, null=True, blank=True)  # Update the unit field to be nullable
    price = models.TextField(max_length=200)

    def __str__(self):
        return self.name
    
class purchaseFormData(models.Model):
    bill = models.TextField(max_length=200)
    vendor = models.ForeignKey(vendorContactForm, on_delete=models.CASCADE)
    product = models.ForeignKey(productFormData, on_delete=models.CASCADE)
    buy = models.TextField(max_length=200)
    type = models.CharField(max_length=200, default='Cash')
    quantity = models.TextField(max_length=200, null=True, blank=True)  
    sell = models.TextField(max_length=200)

    def __str__(self):
        return self.bill
    
class StockData(models.Model):
    product = models.ForeignKey(productFormData, on_delete=models.CASCADE)
    total_quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name

class SalesForm(models.Model):
    customer = models.ForeignKey(CustomerContactForm, on_delete=models.CASCADE)
    employee = models.ForeignKey(employeeContactForm, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=200, default="Cash")

    def __str__(self):
        return f"{self.customer.name} - {self.employee.name}"

class SaleItem(models.Model):
    sales_form = models.ForeignKey(SalesForm, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    type = models.CharField(max_length=200, default="Cash")

class accountData(models.Model):
    date = models.DateField(auto_now_add=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=200, default="Cash")

    def __str__(self):
        return f"{self.date} - {self.type}"
    
class Transaction(models.Model):
    purchase = models.ForeignKey(purchaseFormData, on_delete=models.CASCADE, null=True, blank=True)
    sale = models.ForeignKey(SaleItem, on_delete=models.CASCADE, null=True, blank=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=200, default="Cash")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.type}"
    
class expenseData(models.Model):
    expense = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)