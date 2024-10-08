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
        unit = request.POST.get('unit')
        price = request.POST.get('price')

        data = productFormData.objects.create(product=category, name=name, unit=unit, price=price)
        return redirect('/product')
    return render(request, 'productForm.html', {'data': categories})

def updatePageProduct(request, id):
    data = productFormData.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        
        data.name = name
        data.unit = unit if unit else None  # Update the unit field to be nullable
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
        total_purchase_quantity = 0
        for purchase in purchases:
            if purchase.quantity:
                total_purchase_quantity += int(purchase.quantity)
        if product.unit:
            stock_quantity = int(product.unit) + total_purchase_quantity
            if stock_quantity < 0:
                stock_quantity = 0
        else:
            stock_quantity = 0
        StockData.objects.create(product=product, total_quantity=stock_quantity, selling_price=product.price)
    stocks = StockData.objects.all()
    return render(request, 'stock.html', {'products': products, 'stocks': stocks})

def deleteDataStock(request, id):
    data = StockData.objects.get(id=id)
    data.delete()
    return redirect('/stock')

from django.shortcuts import render,redirect
from .models import *

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

def deleteDataSales(request, id):
    data = SalesForm.objects.get(id=id)
    data.delete()
    return redirect('/sales')

def deleteDataSaleItem(request, id):
    data = SaleItem.objects.get(id=id)
    data.delete()
    return redirect('/sales')

def saleItem(request):
    sale_items = SaleItem.objects.all()
    return render(request, 'saleItem.html', {'sale_items': sale_items})

def accounts(request):
    transactions = Transaction.objects.all()
    total_debit = sum(transaction.debit for transaction in transactions)
    total_credit = sum(transaction.credit for transaction in transactions)
    return render(request, 'accounts.html', {'transactions': transactions, 'total_debit': total_debit, 'total_credit': total_credit})

def deleteDataAccounts(request, id):
    data = accountData.objects.get(id=id)
    data.delete()
    return redirect('/accounts')