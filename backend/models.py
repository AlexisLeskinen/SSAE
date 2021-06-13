from django.db import models

# 楼宇信息
buildings = [("C"+str(_), "C"+str(_)) for _ in range(13)]
# 员工类别
workerType = [("0", "总仓管理员"), ("1", "分仓管理员"), ("2", "分仓工作人员")]

# 公共的用户信息


class BaseInfo(models.Model):
    name = models.CharField(max_length=10, verbose_name="姓名")
    sex = models.CharField(max_length=1, verbose_name="性别",
                           choices=[("男", "男"), ("女", "女")])
    phone = models.CharField(max_length=11, verbose_name="手机")
    building = models.CharField(
        max_length=5, choices=buildings, default="C0")
    password = models.CharField(
        max_length=8, verbose_name="密码", default="0000")

    class Meta:
        abstract = True

    def toJson(self) -> dict:
        return {
            "name": self.name,
            "sex": self.sex,
            "phone": self.phone,
            "building": self.building,
            "password": self.password
        }

# 收件人    单例类


class Receiver(BaseInfo):
    receive_id = models.CharField(
        max_length=5, verbose_name="收件人id", primary_key=True)
    self_service = models.BooleanField(verbose_name="自助取件")
    building = models.CharField(
        verbose_name="收件地址", max_length=5, choices=buildings, default="C0")
    door = models.CharField(verbose_name="宿舍门牌号",
                            max_length=4, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"收件人"
        verbose_name_plural = u"收件人"

    def toJson(self) -> dict:
        res = super().toJson()
        res.update({
            "receive_id": self.receive_id,
            "self_service": self.self_service,
            "door": self.door
        })
        return res


# 管理员、员工  单例类


class WareHouseWorker(BaseInfo):
    employee_id = models.CharField(
        max_length=5, verbose_name="员工id", primary_key=True)
    level = models.CharField(
        max_length=2, verbose_name="职工类别", choices=workerType)
    building = models.CharField(
        verbose_name="负责的楼宇", max_length=5, choices=buildings, default="C0")

    def __str__(self):
        return self.building + "-" + self.employee_id + "-" + self.name

    class Meta:
        verbose_name = u"工作人员"
        verbose_name_plural = u"工作人员"

    def toJson(self) -> dict:
        res = super().toJson()
        res.update({
            "employee_id": self.employee_id,
            "level": self.level
        })
        return res

# 快递信息   单例类


class Express(models.Model):
    # id
    express_id = models.CharField(
        verbose_name="快递ID", max_length=7, primary_key=True)
    is_notified = models.BooleanField(verbose_name="是否已通知楼宇管理员", default=False)
    is_divided = models.BooleanField(verbose_name="已分发到对应楼宇", default=False)
    # 收件人
    receiver = models.ForeignKey(
        Receiver, on_delete=models.DO_NOTHING)
    # 位置号 （A5-2-2210）
    locate = models.CharField(
        verbose_name="位置号", max_length=9, blank=True, null=True)
    # 签收时间
    receive_date = models.DateTimeField(
        verbose_name="签收时间", blank=True, null=True)

    # 后台管理名称
    class Meta:
        verbose_name = u"快递信息"
        verbose_name_plural = u"快递信息"

    def __str__(self):
        return self.express_id + "-" + self.receiver.name

    def change(self, **kwgs) -> bool:
        """
        @description: 
        动态修改快递信息，配合save更新数据
        ---------
        @param: 下面四个参数的dict
        -------
        @Returns: 是否更新了字段
        -------
        """
        c = False
        for k, v in kwgs.items():
            if("is_notified" == k):
                self.is_notified = v
                c = True
            if("is_divided" == k):
                self.is_divided = v
                c = True
            if("locate" == k):
                self.locate = v
                c = True
            if("receive_date" == k):
                self.receive_date = v
                c = True
        return c

    def state(self) -> str:
        """
        @description: 
        动态生成当前快递状态
        -------
        @Returns: str 快递状态
        -------
        """

        state = "快递"
        if(self.receive_date):
            state += "已于"+str(self.receive_date)+"签收"
        elif(self.locate):
            state += "在" + self.receiver.building + "-" + self.locate
        elif(self.is_divided):
            state += "已分发至"+self.receiver.building+"仓库"
        elif(self.is_notified):
            state += "已通知分发"
        else:
            state += "未通知分发"

        return state

    def toJson(self) -> dict:
        return {
            "express_id": self.express_id,
            "is_notified": self.is_notified,
            "is_divided": self.is_divided,
            "name": self.receiver.name,
            "phone": self.receiver.phone,
            "self_service": self.receiver.self_service,
            "s_s_t": '是' if(self.receiver.self_service)else'否',
            "building": self.receiver.building,
            "door": self.receiver.door,
            "state": self.state(),
            "locate": self.locate,
            "receive_date": self.receive_date,
        }
