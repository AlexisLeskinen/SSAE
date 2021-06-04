import json
from backend.models import ExpressInfo
from django.http.response import HttpResponse, JsonResponse
from django.core import serializers
import random
# 假数据生成包
from faker import Faker
# Create your views here.


def test(request):
   
    return JsonResponse("data", safe=False, json_dumps_params={'ensure_ascii': False})

# 将Django的model对象的feild部分序列化成json


def modelToJson(model):
    queryset = serializers.serialize("json", model.objects.all())
    queryset = json.loads(queryset)
    data = []
    for i in queryset:
        data.append(i["fields"])
# JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    return data

# 随机生成快递数据，写入数据库


def generalExpress(request):
    fake = Faker("zh_CN")

    name = fake.name()
    id = str(random.randrange(1, 10000000)).zfill(7)
    building = "C" + str(random.randint(1, 12))
    phone = fake.phone_number()

    E = ExpressInfo(express_id=id, receiver=name,
                    building=building, phone=phone)
    E.save()

    return HttpResponse(E.express_id)
