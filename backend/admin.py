from backend.models import ExpressInfo, MainWareHouseAdmin, Receiver, WareHouseWorker
from django.contrib import admin

# Register your models here.


class ExpressList(admin.ModelAdmin):
    list_display = ['express_id']


class MWAdminList(admin.ModelAdmin):
    list_display = ['employee_id']


class WokerList(admin.ModelAdmin):
    list_display = ['employee_id']


class ReceiverList(admin.ModelAdmin):
    list_display = ['receive_id']


admin.site.register(ExpressInfo, ExpressList)
admin.site.register(MainWareHouseAdmin, MWAdminList)
admin.site.register(WareHouseWorker, WokerList)
admin.site.register(Receiver, ReceiverList)
