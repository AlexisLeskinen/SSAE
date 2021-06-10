from backend.models import *
from django.contrib import admin

# Register your models here.


class ExpressList(admin.ModelAdmin):
    list_display = ('express_id', 'receiver')


class WareHouseWorkerList(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'sex')


class ReceiverList(admin.ModelAdmin):
    list_display = ('receive_id', 'name', 'phone')


admin.site.register(Express, ExpressList)
admin.site.register(WareHouseWorker, WareHouseWorkerList)
admin.site.register(Receiver, ReceiverList)
