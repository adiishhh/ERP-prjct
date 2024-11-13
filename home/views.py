from django.shortcuts import render,redirect
from .models import *
from decimal import Decimal

def home(request):
    return render(request, 'index.html')

def customer(request):
    customer = CustomerContactForm.objects.all()
    return render(request, 'customer.html', {'customer': customer})

def customerForm(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        place = request.POST.get('place')
        
    
        data = CustomerContactForm.objects.create(name=name, phone=phone, email=email, place=place)
        return redirect('/customer')
    return render(request, 'customerForm.html')

def updatePage(request, id):
    data = CustomerContactForm.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        place = request.POST.get('place')
        
        
        data.name = name
        data.phone = phone
        data.email = email
        data.place = place
        data.save()
        return redirect('/customer')
    return render(request, 'updatePage.html', {'data': data})


def deleteData(request,id):
    data=CustomerContactForm.objects.get(id=id)
    data.delete()
    return redirect('/customer')

def employee(request):
    employee = employeeContactForm.objects.all()
    return render(request, 'employee.html', {'employee': employee})

def employeeForm(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        place = request.POST.get('place')
        salary = request.POST.get('salary')
        
    
        data = employeeContactForm.objects.create(name=name, phone=phone, email=email, place=place, salary=salary)
        return redirect('/employee')
    return render(request, 'employeeForm.html')

def updateEmployee(request, id):
    data = employeeContactForm.objects.get(id=id)
    if request.method == 'POST':
        data.name = request.POST.get('name')
        data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.place = request.POST.get('place')
        data.salary = request.POST.get('salary')
        data.save()
        return redirect('/employee')
    return render(request, 'updateEmployee.html', {'data': data})

def deleteEmployee(request, id):
    data = employeeContactForm.objects.get(id=id)
    data.delete()
    return redirect('/employee')

def category(request):
    category = categoryFormData.objects.all()
    return render(request, 'category.html', {'category': category})

def categoryForm(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        
        data = categoryFormData.objects.create(name=name)
        return redirect('/category')
    return render(request, 'categoryForm.html')

def deleteCategory(request, id):
    data = categoryFormData.objects.get(id=id)
    data.delete()
    return redirect('/category')

def vendor(request):
    vendor = vendorContactForm.objects.all()
    return render(request, 'vendor.html', {'vendor': vendor})

def vendorForm(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
    
        data = vendorContactForm.objects.create(name=name, phone=phone, email=email)
        return redirect('/vendor')
    return render(request, 'vendorForm.html')

def deleteDataVendor(request, id):
    data = vendorContactForm.objects.get(id=id)
    data.delete()
    return redirect('/vendor')

def product(request):
    product = productFormData.objects.all()
    return render(request, 'product.html', {'product': product})

def productForm(request):
    categories = categoryFormData.objects.all()
    if request.method == 'POST':
        category = categoryFormData.objects.get(id=request.POST.get('category'))
        name = request.POST.get('name')
        # unit = request.POST.get('unit')
        price = request.POST.get('price')

        data = productFormData.objects.create(product=category, name=name, price=price)
        return redirect('/product')
    return render(request, 'productForm.html', {'data': categories})

def updatePageProduct(request, id):
    data = productFormData.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        # unit = request.POST.get('unit')
        price = request.POST.get('price')
        
        data.name = name
        # data.unit = unit if unit else None  # Update the unit field to be nullable
        data.price = price
        data.save()
        return redirect('/product')
    return render(request, 'updateProduct.html', {'data': data})

def deleteDataProduct(request, id):
    data = productFormData.objects.get(id=id)
    data.delete()
    return redirect('/product')

def purchase(request):
    purchase = purchaseFormData.objects.all()
    return render(request, 'purchase.html', {'purchase': purchase})

def purchaseForm(request):
    vendor_list = vendorContactForm.objects.all()
    product_list = productFormData.objects.all()
    if request.method == 'POST':
        vendor = vendorContactForm.objects.get(id=request.POST.get('selectVendor'))
        product = productFormData.objects.get(id=request.POST.get('selectProduct'))
        bill = request.POST.get('bill')
        buy_price = request.POST.get('buy_price')
        type = request.POST.get('type')
        quantity = request.POST.get('quantity')
        sell_price = request.POST.get('sell_price')

        data = purchaseFormData.objects.create(vendor=vendor, product=product, bill=bill, buy=buy_price,type = type ,quantity=quantity, sell=sell_price)
        Transaction.objects.create(purchase=data, debit=Decimal(buy_price) * Decimal(quantity), credit=0, type=type)
        return redirect('/purchase')
    return render(request, 'purchaseForm.html', {'vendor_list': vendor_list, 'product_list': product_list})


def deleteDataPurchase(request, id):
    data = purchaseFormData.objects.get(id=id)
    data.delete()
    return redirect('/purchase')

def stock(request):
    products = productFormData.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product')
        product = productFormData.objects.get(id=product_id)
        
        purchases = purchaseFormData.objects.filter(product=product)
        total_purchase_quantity = sum(int(purchase.quantity) for purchase in purchases if purchase.quantity)
        
        sales = SaleItem.objects.filter(stock__product=product)
        total_sale_quantity = sum(int(sale.quantity) for sale in sales if sale.quantity)
        
        if product.unit:
            total_quantity = int(product.unit) + total_purchase_quantity - total_sale_quantity
        else:
            total_quantity = total_purchase_quantity - total_sale_quantity
        
        stock_data, created = StockData.objects.get_or_create(product=product, defaults={'total_quantity': total_quantity, 'selling_price': product.price})
        
        if not created:
            stock_data.total_quantity = total_quantity
            stock_data.selling_price = product.price
            stock_data.save()
    
    stocks = StockData.objects.all()
    return render(request, 'stock.html', {'products': products, 'stocks': stocks})

def deleteDataStock(request, id):
    data = StockData.objects.get(id=id)
    data.delete()
    return redirect('/stock')

def sales(request):
    sales = SalesForm.objects.all()
    return render(request, 'sales.html', {'sales': sales})

def salesForm(request):
    customer_list = CustomerContactForm.objects.all()
    employee_list = employeeContactForm.objects.all()
    if request.method == 'POST':
        customer = CustomerContactForm.objects.get(id=request.POST.get('selectCustomer'))
        employee = employeeContactForm.objects.get(id=request.POST.get('selectEmployee'))
        sales_form = SalesForm.objects.create(customer=customer, employee=employee)
        return redirect('/salesItemForm/' + str(sales_form.id))
    return render(request, 'salesForm.html', {'customer_list': customer_list, 'employee_list': employee_list})

def deleteDataSales(request, id):
    data = SalesForm.objects.get(id=id)
    data.delete()
    return redirect('/sales')

def saleItem(request):
    sale_items = SaleItem.objects.all()
    return render(request, 'saleItem.html', {'sale_items': sale_items})

def salesItemForm(request, id):
    sales_form = SalesForm.objects.get(id=id)
    stock_list = StockData.objects.all()
    if request.method == 'POST':
        stock = StockData.objects.get(id=request.POST.get('selectStock'))
        quantity = int(request.POST.get('quantity'))
        type = request.POST.get('type')
        sales_form.type = type
        sales_form.save()
        sale_item = SaleItem.objects.create(sales_form=sales_form, stock=stock, quantity=quantity, type=type)
        if stock.total_quantity >= quantity:
            stock.total_quantity -= quantity
            stock.save()
            sales_form.total_amount += Decimal(stock.selling_price) * Decimal(quantity)
            sales_form.save()
            Transaction.objects.create(sale=sale_item, debit=0, credit=sales_form.total_amount, type=type)
            return redirect('/sales') 
        else:
            return redirect('/salesItemForm/' + str(sales_form.id))
    return render(request, 'salesItemForm.html', {'stock_list': stock_list, 'sales_form': sales_form})


def deleteDataSaleItem(request, id):
    data = SaleItem.objects.get(id=id)
    data.delete()
    return redirect('/sales')


def accounts(request):
    transactions = Transaction.objects.all()
    account_data = accountData.objects.all()
    total_debit = sum(transaction.debit for transaction in transactions) + sum(data.debit for data in account_data)
    total_credit = sum(transaction.credit for transaction in transactions) + sum(data.credit for data in account_data)
    return render(request, 'accounts.html', {'transactions': transactions, 'account_data': account_data, 'total_debit': total_debit, 'total_credit': total_credit})

def deleteDataAccounts(request, id):
    data = accountData.objects.get(id=id)
    data.delete()
    return redirect('/accounts')

def expense(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        expense = expenseData.objects.create(name=name, amount=amount)
        accountData.objects.create(debit=Decimal(amount), credit=0, type="Expense")
        return redirect('/expense')
    expense = expenseData.objects.all()
    return render(request, 'expense.html', {'expense': expense})

def expenseForm(request):
    if request.method == 'POST':
        expense = request.POST.get('expense')
        amount = request.POST.get('amount')
        data = expenseData.objects.create(expense=expense, amount=amount)
        accountData.objects.create(debit=Decimal(amount), credit=0, type="Expense")
        return redirect('/expense')
    return render(request, 'expenseForm.html')

def deleteExpense(request, id):
    expense = expenseData.objects.get(id=id)
    account_data = accountData.objects.filter(type="Expense", debit=expense.amount)
    if account_data.exists():
        account_data.delete()
    expense.delete()
    return redirect('/expense')




# _____________________________________________- REST API-__________________________________________________




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *


class Customer(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return CustomerContactForm.objects.all()
    def get(self, request):
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return CustomerContactForm.objects.get(pk=pk)
        except CustomerContactForm.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerPostSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Employee(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return employeeContactForm.objects.all()

    def get(self, request):
        employees = self.get_queryset()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return employeeContactForm.objects.filter(pk=pk).first()

    def get(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeePostSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Category(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return categoryFormData.objects.all()

    def get(self, request):
        categories = self.get_queryset()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return categoryFormData.objects.filter(pk=pk).first()

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryPostSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Vendor(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return vendorContactForm.objects.all()

    def get(self, request):
        vendors = self.get_queryset()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return vendorContactForm.objects.filter(pk=pk).first()

    def get(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorPostSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class  Product(APIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return productFormData.objects.all()

    def get(self, request):
        products = self.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Get the category ID from the request data
        category_id = request.data.get('product')

        # Retrieve the category instance using the ID
        try:
            category = categoryFormData.objects.get(pk=category_id)
        except categoryFormData.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the product with the category instance
        serializer = ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=category)  # Save the product with the category instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return productFormData.objects.filter(pk=pk).first()

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductPostSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Purchase(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return purchaseFormData.objects.all()

    def get(self, request):
        purchases = self.get_queryset()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchasePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return purchaseFormData.objects.filter(pk=pk).first()

    def get(self, request, pk):
        purchase = self.get_object(pk)
        if purchase is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase = self.get_object(pk)
        if purchase is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchasePostSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase = self.get_object(pk)
        if purchase is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Stock(APIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return StockData.objects.all()

    def get(self, request):
        stocks = self.get_queryset()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product')
        product = productFormData.objects.get(id=product_id)
        
        purchases = purchaseFormData.objects.filter(product=product)
        total_purchase_quantity = sum(int(purchase.quantity) for purchase in purchases if purchase.quantity)
        
        sales = SaleItem.objects.filter(stock__product=product)
        total_sale_quantity = sum(int(sale.quantity) for sale in sales if sale.quantity)
        
        # Removed the unit check
        total_quantity = total_purchase_quantity - total_sale_quantity
        
        stock_data, created = StockData.objects.get_or_create(product=product, defaults={'total_quantity': total_quantity, 'selling_price': product.price})
        
        if not created:
            stock_data.total_quantity = total_quantity
            stock_data.selling_price = product.price
            stock_data.save()
        
        serializer = StockPostSerializer(stock_data)
        return Response(serializer.data)

class StockDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return StockData.objects.filter(pk=pk).first()

    def get(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def put(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StockPostSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Sales(APIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SalesForm.objects.all()

    def get(self, request):
        sales = self.get_queryset()
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SalesPostSerializer(data=request.data)
        if serializer.is_valid():
            sale = serializer.save() 

           
            product_id = request.data.get('product')
            try:
                product = productFormData.objects.get(id=product_id)  
            except productFormData.DoesNotExist:
                return Response({"error": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            stock_id = request.data.get('product') 
            try:
                stock = StockData.objects.get(product__id=stock_id) 
            except StockData.DoesNotExist:
                return Response({"error": "Stock does not exist for the selected product."}, status=status.HTTP_400_BAD_REQUEST)
            
            sale_item_data = {
                'sales_form': sale.id,  
                'stock': stock.id, 
                'quantity': request.data.get('quantity'),  
            }
            sale_item_serializer = SaleItemSerializer(data=sale_item_data)
            if sale_item_serializer.is_valid():
                sale_item_serializer.save() 
                return Response(sale_item_serializer.data, status=status.HTTP_201_CREATED) 
            else:
                print("SaleItem errors:", sale_item_serializer.errors)  
                return Response(sale_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("Sales errors:", serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        return SalesForm.objects.filter(pk=pk).first()

    def get(self, request, pk):
        sales = self.get_object(pk)
        if sales is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SalesSerializer(sales)
        return Response(serializer.data)

    def delete(self, request, pk):
        sales = self.get_object(pk)
        if sales is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SaleItemView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

    
class SalesItemFormView(generics.UpdateAPIView):
    queryset = SalesForm.objects.all()
    serializer_class = SalesFormSerializer

    def update(self, request, *args, **kwargs):
        sales_form = self.get_object()
        stock = StockData.objects.get(id=request.data.get('selectStock'))
        quantity = int(request.data.get('quantity'))
        type = request.data.get('type')
        sales_form.type = type
        sales_form.save()
        sale_item = SaleItem.objects.create(sales_form=sales_form, stock=stock, quantity=quantity, type=type)
        if stock.total_quantity >= quantity:
            stock.total_quantity -= quantity
            stock.save()
            sales_form.total_amount += Decimal(stock.selling_price) * Decimal(quantity)
            sales_form.save()
            Transaction.objects.create(sale=sale_item, debit=0, credit=sales_form.total_amount, type=type)
            return Response({'message': 'Sale item created successfully'})
        else:
            return Response({'message': 'Not enough stock'}, status=400)

class DeleteSaleItemView(generics.DestroyAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class Accounts(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Transaction.objects.all()

    def get_serializer(self):
        return TransactionSerializer

    def get(self, request):
        transactions = self.get_queryset()
        serializer = self.get_serializer()(transactions, many=True)
        account_data = accountData.objects.all()
        serializer_account_data = AccountSerializer(account_data, many=True)
        total_debit = sum(transaction.debit for transaction in transactions) + sum(data.debit for data in account_data)
        total_credit = sum(transaction.credit for transaction in transactions) + sum(data.credit for data in account_data)
        return Response({
            'transactions': serializer.data,
            'account_data': serializer_account_data.data,
            'total_debit': total_debit,
            'total_credit': total_credit
        })

class AccountDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return accountData.objects.get(pk=pk)
        except accountData.DoesNotExist:
            return None

    def get(self, request, pk):
        account_data = self.get_object(pk)
        if account_data is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(account_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        account_data = self.get_object(pk)
        if account_data is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Expense(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return expenseData.objects.all()

    def get_serializer(self):
        return ExpenseSerializer

    def post(self, request):
        expense = request.data.get('expense')
        amount = request.data.get('amount')
        expenseData.objects.create(expense=expense, amount=amount)
        accountData.objects.create(debit=Decimal(amount), credit=0, type="Expense")
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        expense = self.get_queryset()
        serializer = self.get_serializer()(expense, many=True)
        return Response(serializer.data)

class ExpenseForm(APIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return expenseData.objects.all()

    def get_serializer(self):
        return ExpenseSerializer

    def post(self, request):
        expense = request.data.get('expense')
        amount = request.data.get('amount')
        data = expenseData.objects.create(expense=expense, amount=amount)
        accountData.objects.create(debit=Decimal(amount), credit=0, type="Expense")
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        expense = self.get_queryset()
        serializer = self.get_serializer()(expense, many=True)
        return Response(serializer.data)

class DeleteExpense(APIView):
    permission_classes = [AllowAny]  # Adjust this as needed

    def get_queryset(self):
        return expenseData.objects.all()

    def get_object(self, pk):
        try:
            return expenseData.objects.get(pk=pk)
        except expenseData.DoesNotExist:
            return None

    def delete(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account_data = accountData.objects.filter(type="Expense", debit=expense.amount)
        if account_data.exists():
            account_data.delete()
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)