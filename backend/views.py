from backend.models import ExpressInfo, Receiver, WareHouseWorker
from django.http.response import HttpResponse, JsonResponse
from django.core import serializers
import random
import json
# 假数据生成包
from faker import Faker
# Create your views here.


def test(request):
    data = modelToJson(ExpressInfo)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

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


def generalReceiver(request):
    Einfos = modelToJson(ExpressInfo)

    for e in Einfos:
        name = e['receiver']
        sex = "男女"[random.randrange(0, 2)]
        phone = e['phone']
        id = str(random.randrange(1, 100000000)).zfill(8)
        selfservice = random.randrange(0, 2)
        building = e['building']
        R = Receiver(name=name, sex=sex, phone=phone,
                     receive_id=id, self_service=selfservice,
                     building=building
                     )
        R.save()

    return JsonResponse(modelToJson(Receiver), safe=False, json_dumps_params={'ensure_ascii': False})


# 随机生成分仓人员
def generalWarehouseWorker(request):
    fake = Faker("zh_CN")

    for i in range(13):
        name = fake.name()
        id = str(random.randrange(1, 100000)).zfill(5)
        phone = fake.phone_number()
        sex = "男女"[random.randrange(0, 2)]
        building = "C" + str(i)
        level = 1

        W = WareHouseWorker(name=name, sex=sex,
                            phone=phone, level=level,
                            building=building, employee_id=id)
        W.save()
    
    return JsonResponse(modelToJson(WareHouseWorker), safe=False, json_dumps_params={'ensure_ascii': False})