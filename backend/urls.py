# 后台api分发
from backend.views import *
from django.urls import path


# 这里添加api后面的url操作
urlpatterns = [
    path('test', test),
    path('login', loginHandle),
    path('get-express', getExpress),
    path('get-warehouse', getWareHouse),
    path('handout-express', expressHandOUt),
]
