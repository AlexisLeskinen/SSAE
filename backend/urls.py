# 后台api分发
from backend.views import *
from django.urls import path


# 这里添加api后面的url操作
urlpatterns = [
    path('test', test),
    path('log-in', loginVerify),
    path('admin-type', getAdminType),
    path('log-out', logOut),
    path('get-express', getExpress),
    path('get-warehouse', getWareHouse),
    path('express-update', expressUpdate),
    path('express-received', receivedExpresss),
    path('express-handon', handonExpresss),
    path('new-reciver', newReciver),
    path('new-worker', newWorker),
    path('new-express', newExpress),
]
