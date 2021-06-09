from backend.models import ExpressInfo, MainWareHouseAdmin, Receiver, WareHouseWorker
from django.http.response import Http404, HttpResponse, JsonResponse
from django.core import serializers
import random
import json
# 假数据生成包
from faker import Faker
# Create your views here.


def test(request):
    t = ExpressInfo.objects.all()[:5:1]
    data = list(t)

    return HttpResponse(data)

# 前端请求分发快递，参数为id数组


def expressHandOut(request):
    res = None
    data = json.loads(request.body)
    if(len(data) == 0):
        res = "没有要通知的快递！"
    else:
        for d in data:
            E = ExpressInfo.objects.get(pk=d['id'])
            E.is_notified = True
            E.save()
        res = data[0]['id']+"等"+str(len(data))+"个快递已通知成功！"

    return HttpResponse(res)

# 仓库管理员登陆


def loginHandle(request):
    param = json.loads(request.body)
    res = None
    user = WareHouseWorker.objects.filter(employee_id=param['account'])
    if(len(user)):
        res = {
            'type': 1,
            'building': user[0].building
        }
    else:
        user = MainWareHouseAdmin.objects.filter(employee_id=param['account'])
        if(len(user)):
            res = {
                'type': 0
            }

    return JsonResponse(res)

# 获取所有仓库


def getWareHouse(request):
    queryset = ExpressInfo.objects.values(
        'building').distinct().order_by('building')
    data = list(queryset)

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

# 返回快递信息


def getExpress(request):
    param = json.loads(request.body)
    queryset = ExpressInfo.objects.filter(**param)
    return toJson(queryset)

# 将Django的model对象的feild部分序列化成json
# 注意里面将primarykey的标识改为id了


def toJson(queryset):
    tempdata = serializers.serialize("json", queryset)
    tempdata = json.loads(tempdata)
    data = []
    for d in tempdata:
        d["fields"]["id"] = d["pk"]
        data.append(d["fields"])
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


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
    Einfos = toJson(ExpressInfo)

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

    return HttpResponse("!")


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

    return HttpResponse("!")
