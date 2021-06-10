# 后台api分发
from backend.views import *
from django.urls import path


# 这里添加api后面的url操作
urlpatterns = [
    path('test', test),
    path('login', loginVerify),
    path('get-express', getExpress),
    path('get-warehouse', getWareHouse),
    path('express-update', expressUpdate),
    path('new-reciver', newReciver),
    path('new-worker', newWorker),
    path('new-express', newExpress),
]
