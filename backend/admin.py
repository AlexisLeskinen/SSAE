from backend.models import *
from django.contrib import admin

# Register your models here.


class ExpressList(admin.ModelAdmin):
    list_display = ('express_id', 'receiver')


class MWAdminList(admin.ModelAdmin):
    list_display = ('employee_id', 'name')


class WWokerList(admin.ModelAdmin):
    list_display = ('employee_id', 'name')


class ReceiverList(admin.ModelAdmin):
    list_display = ('receive_id', 'name')


admin.site.register(ExpressInfo, ExpressList)
admin.site.register(MainWareHouseAdmin, MWAdminList)
admin.site.register(WareHouseWorker, WWokerList)
admin.site.register(Receiver, ReceiverList)
