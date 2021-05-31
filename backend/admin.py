from backend.models import ExpressInfo
from django.contrib import admin

# Register your models here.


class ExpressList(admin.ModelAdmin):
    list_display = ['express_id']


admin.site.register(ExpressInfo, ExpressList)
