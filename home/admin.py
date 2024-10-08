from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomerContactForm)
admin.site.register(employeeContactForm)
admin.site.register(categoryFormData)
admin.site.register(vendorContactForm)
admin.site.register(productFormData)
admin.site.register(purchaseFormData)
admin.site.register(StockData)
admin.site.register(SalesForm)
admin.site.register(SaleItem)
admin.site.register(accountData)
admin.site.register(Transaction)
admin.site.register(expenseData)