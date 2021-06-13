# 后台api分发
from backend.views import *
from django.urls import path


# 这里添加api后面的url操作
urlpatterns = [
    path('test', test),
    # 登陆
    path('log-in', loginVerify),
    # 获取工作人员信息
    path('admin-type', getAdminType),
    # 登出
    path('log-out', logOut),
    # 获取快递
    path('get-express', getExpress),
    # 获取仓库列表
    path('get-warehouse', getWareHouse),
    # 更新快递信息
    path('express-update', expressUpdate),
    # 快递签收
    path('express-received', receivedExpresss),
    # 快递上架
    path('express-handon', handonExpresss),
    # 用户登陆
    path('user-login', userLogin),
    # 用户注册/修改
    path('user-save', saveReceiver),
    # 用户获取
    path('get-user', getReceiver),

    # 随机生成数据
    path('new-reciver', newReciver),
    path('new-worker', newWorker),
    path('new-express', newExpress),
]
