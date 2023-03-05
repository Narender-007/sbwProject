from django.contrib import admin

# Register your models here.

from buswalaApp.models import sbw_customer,sbw_driver,sbw_review,sbw_bookingOrder
admin.site.register(sbw_customer)
admin.site.register(sbw_driver)
admin.site.register(sbw_review)
admin.site.register(sbw_bookingOrder)
