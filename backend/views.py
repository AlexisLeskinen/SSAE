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


def resultReturn(data=[], msg: str = "操作成功!", code: int = 200):
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
        'code': code,
        'data': data
    }

    return JsonResponse(res, json_dumps_params={'ensure_ascii': False})


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
                E = Express.objects.get(pk=d['express_id'])
                E.change(**d)
                E.save()
            res = param[0]['express_id']+"等"+str(len(param))+"个快递更新成功！"

    return resultReturn(msg=res)


def loginVerify(request):
    """
    @description:
    登陆验证，验证员工id是否存在，并保存cookie
    ---------
    @param: 帐号和密码的json
    -------
    @Returns: 
    -------
    """
    cookie = None
    msg = ""
    code = 200
    param = json.loads(request.body)
    quryset = WareHouseWorker.objects.filter(
        employee_id=param['account'], password=param['password'])
    if(len(quryset)):
        cookie = param['account']
        msg = param['account']+"登陆成功！"
    else:
        msg = "帐号或密码错误！"
        code = 400
    res = resultReturn(msg=msg, code=code)
    res.set_cookie("user", cookie)
    return res


def getAdminType(request):
    """
    @description: 
    根据cookie获取登陆的管理员类型
    ---------
    @param: 无
    -------
    @Returns: 
    -------
    """

    admin = request.COOKIES.get("user")
    W = WareHouseWorker.objects.get(pk=admin)
    code = 200
    res = {}
    if(int(W.level) < 2):
        res = {
            "type": W.level,
            "building": W.building,
            "user": W.employee_id + W.name
        }
    else:
        code = 400

    return resultReturn(data=res, code=code)


def logOut(request):
    """
    @description: 
    账号登出，删除对应的cookie
    ---------
    @param: 带有cookie的request
    -------
    @Returns: 
    -------
    """

    user = request.COOKIES.get("user")
    res = resultReturn(msg=user+"登出成功！")
    res.delete_cookie("user")

    return res


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
    l = []
    for b in buildings:
        l.append(b[0])
    l.pop(0)

    return resultReturn(l)


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
        if(Receiver.objects.filter(receive_id=r['receive_id']).count() == 0):
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
        if(WareHouseWorker.objects.filter(employee_id=w['employee_id']).count() == 0):
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
        if(Express.objects.filter(express_id=e['express_id']).count() == 0):
            t = Express(**e)
            t.save()
    after = Express.objects.count()
    return resultReturn(msg="成功生成"+str(after-before)+"个快递！")
