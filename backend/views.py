from backend.models import Express, Receiver, WareHouseWorker, buildings
from django.http.response import HttpResponse, JsonResponse
from backend.DataGenerator import G
import json


def test(request):
    E = Express.objects.first()
    kwgs = {
        "locate": "A1-2-5531"
    }
    E.change(**kwgs)
    E.save()
    return resultReturn(E.toJson())


def resultReturn(data=[], msg="操作成功!"):
    """
    @description: 
    封装了一下返回结果
    ---------
    @param: data是一个json，msg是提示信息
    -------
    @Returns: 
    -------
    """

    res = {
        'msg': msg,
        'data': data
    }

    return JsonResponse(res)


def expressUpdate(request):
    """
    @description: 
    更新快递通知状态、分发状态等
    ---------
    @param: 更新字段的json数组
    -------
    @Returns: 
    -------
    """

    res = None
    if(request.body):
        param = json.loads(request.body)
        if(len(param) == 0):
            res = "没有要更新的快递！"
        else:
            for d in param:
                E = Express.objects.get(pk=d['id'])
                E.change(**d)
                E.save()
            res = param[0]['id']+"等"+str(len(param))+"个快递更新知成功！"

    return resultReturn(msg=res)


def loginVerify(request):
    """
    @description: 
    登陆验证，验证员工id是否存在标注
    ---------
    @param: 帐号和密码的json
    -------
    @Returns: 员工类型和所属仓库
    -------
    """

    param = json.loads(request.body)
    res = {}
    quryset = WareHouseWorker.objects.filter(
        employee_id=param['account'], password=param['password'])
    if(len(quryset)):
        account = quryset[0]
        res = {
            'type': account.level,
            'building': account.building
        }

    return resultReturn(data=res)


def getWareHouse(request):
    """
    @description: 
    获取所有仓库信息
    ---------
    @param: 无
    -------
    @Returns: (C1,C1)类型的数组
    -------
    """

    return resultReturn(buildings)


def getExpress(request):
    """
    @description: 
    获取快递信息
    ---------
    @param: 包含要查询字段的json
    -------
    @Returns: Json
    -------
    """

    param = json.loads(request.body)
    queryset = Express.objects.filter(**param)
    data = []
    for q in queryset:
        data.append(q.toJson())
    return resultReturn(data=data)


def newReciver(request):
    """
    @description: 
    随机生成收件人
    ---------
    @param: get请求中的num参数
    -------
    @Returns: 
    -------
    """
    param = request.GET
    num = int(param['num'])

    Rs = G.receiver(num)
    before = Receiver.objects.count()
    for r in Rs:
        if(Receiver.objects.filter(r['receive_id']).count == 0):
            t = Receiver(**r)
            t.save()
    after = Receiver.objects.count()
    return resultReturn(msg="成功生成"+str(after-before)+"个收件人！")


def newWorker(request):
    """
    @description: 
    随机生成工作人员
    ---------
    @param: get请求中的num参数
    -------
    @Returns: 
    -------
    """

    param = request.GET
    num = int(param['num'])
    Ws = G.woker(num)
    before = WareHouseWorker.objects.count()
    for w in Ws:
        if(WareHouseWorker.objects.filter(w['employee_id']).count == 0):
            t = WareHouseWorker(**w)
            t.save()
    after = WareHouseWorker.objects.count()
    return resultReturn(msg="成功生成"+str(after-before)+"个工作人员！")


def newExpress(request):
    """
    @description: 
    随机生快递，注意，要先生成收件人
    ---------
    @param: get请求中的num参数
    -------
    @Returns: 
    -------
    """

    param = request.GET
    num = int(param['num'])
    # 如果没有收件人，则先生成
    if(not Receiver.objects.count()):
        newReciver(request)
    Es = G.express(num)
    before = Express.objects.count()
    for e in Es:
        e.update({'receiver': Receiver.objects.order_by("?").first()})
        if(Express.objects.filter(e['express_id']).count == 0):
            t = Express(**e)
            t.save()
    after = Express.objects.count()
    return resultReturn(msg="成功生成"+str(after-before)+"个快递！")
