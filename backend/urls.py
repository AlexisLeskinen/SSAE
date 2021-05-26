# 后台api分发
from django.http.response import HttpResponse
from django.urls import path


def test(request):
    return HttpResponse("test")


# 这里添加api后面的url操作
urlpatterns = [
    path('test', test),
]
