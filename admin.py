
from .models import *
from django.contrib.auth.models import Group
import datetime
from django.contrib.admin.filters import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import decimal, csv
from django.contrib import admin
from django.http import HttpResponse
from django.db.models import F
# Register your models here.
def export_order(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    writer = csv.writer(response)
    writer.writerow(['User ID','Product ID','Address','Amount','Quantity','Date','Status'])
    order = queryset.values_list('user','product','addres','amount','quantity','date','status')
    for book in order:
        writer.writerow(book)
    return response
    export_order.short_description = 'Export to csv'
admin.site.site_header='MobiCart'
class productAdmin(admin.ModelAdmin):
    list_display=('name','title','storage','display','actual_price','offer_price','front_camera','processor','battery')
    list_filter=('name',)
    search_fields = ('title',)

class MyDateTimeFilter(DateFieldListFilter):
    def _init_(self, *args, **kwargs):
        super(MyDateTimeFilter, self)._init_(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()
class orderAdmin(admin.ModelAdmin):
    
    def product_name(self, instance):
        return instance.product.name
    def address_phone(self, instance):
        return instance.addres.mobileno
    def has_add_permission(self, request, obj=None):
        return False
    actions = [
         export_order,]
    list_display=('user','product_name','address_phone','amount','quantity','date','status',)

    list_filter = (
        ('date', MyDateTimeFilter),
    )


class addressAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    list_display=('id','user','name','mobileno','house_name','area','state','pincode')

admin.site.register(product,productAdmin)
admin.site.register(address,addressAdmin)
# admin.site.register(card)
admin.site.register(order,orderAdmin)
admin.site.unregister(Group)