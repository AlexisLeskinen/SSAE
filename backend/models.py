from django.db import models

# 楼宇信息
buildings = [("C"+str(_), "C"+str(_)) for _ in range(13)]
# 员工类别
workerType = [("0", "总仓分仓管理员"), ("1", "分仓管理员"), ("2", "分仓工作人员")]

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

    def toJson(self):
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
        max_length=5, verbose_name="收件人id", primary_key=True, editable=False)
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

    def toJson(self):
        return super().toJson().update({
            "receive_id": self.receive_id,
            "self_service": self.self_service,
            "door": self.door
        })


# 管理员、员工  单例类


class WareHouseWorker(BaseInfo):
    employee_id = models.CharField(
        max_length=5, verbose_name="员工id", primary_key=True, editable=False)
    level = models.CharField(
        max_length=2, verbose_name="职工类别", choices=workerType)
    building = models.CharField(
        verbose_name="负责的楼宇", max_length=5, choices=buildings, default="C0")

    def __str__(self):
        return self.building + "-" + self.employee_id + "-" + self.name

    class Meta:
        verbose_name = u"工作人员"
        verbose_name_plural = u"工作人员"

    def toJson(self):
        return super().toJson().update({
            "employee_id": self.employee_id,
            "level": self.level
        })

# 快递信息   单例类


class Express(models.Model):
    # id
    express_id = models.CharField(
        verbose_name="快递ID", max_length=7, primary_key=True, editable=False)
    is_notified = models.BooleanField(verbose_name="是否已通知楼宇管理员", default=False)
    is_divided = models.BooleanField(verbose_name="已分发到对应楼宇", default=False)
    # 收件人
    receiver = models.OneToOneField(
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

    def change(self, **kwgs):
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

    def toJson(self):
        return {
            "express_id": self.express_id,
            "is_notified": self.is_notified,
            "is_divided": self.is_divided,
            "receiver": {
                "name": self.receiver.name,
                "self_service": self.receiver.self_service,
                "building": self.receiver.building,
                "door": self.receiver.door
            },
            "locate": self.locate,
            "receive_date": self.receive_date,
        }
