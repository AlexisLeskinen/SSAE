from django.db import models

# Create your models here.

# 楼宇信息
builddiingNum = [("C1", "C1"), ("C2", "C2"), ("C3", "C3"), ("C4", "C4"),
                 ("C5", "C5"), ("C6", "C6"), ("C7", "C7"), ("C8", "C8"),
                 ("C9", "C9"), ("C10", "C10"), ("C11", "C11"), ("C12", "C12"), ]
# 员工类别
workerLevel = [("0", "分仓管理员"), ("1", "分仓工作人员")]
# 快递信息


class ExpressInfo(models.Model):
    # id
    express_id = models.CharField(
        verbose_name="快递ID", max_length=10, primary_key=True)
    # 建筑号数
    building = models.CharField(
        verbose_name="楼宇号", max_length=5, choices=builddiingNum)
    # 收件人
    receiver = models.CharField(verbose_name="收件人", max_length=10)
    # 手机
    phone = models.CharField(verbose_name="手机", max_length=12)
    # 备注
    note = models.TextField(verbose_name="备注", blank=True, null=True)
    # 位置号 （A5-2-2210）
    locate = models.CharField(
        verbose_name="位置号", max_length=15, blank=True, null=True)
    # 签收时间
    receive_date = models.DateField(verbose_name="签收时间", blank=True, null=True)

    # 后台管理名称
    class Meta:
        verbose_name = u"快递信息"
        verbose_name_plural = u"快递信息"

    def __str__(self):
        return self.express_id

# 公共的用户信息


class BaseInfo(models.Model):
    name = models.CharField(max_length=10, verbose_name="姓名")
    phone = models.CharField(max_length=12, verbose_name="手机")

    class Meta:
        abstract = True

# 收件人


class Receiver(BaseInfo):
    receive_id = models.CharField(
        max_length=8, verbose_name="收件人id", primary_key=True)
    self_service = models.BooleanField(verbose_name="自助取件")
    building = models.CharField(
        verbose_name="收件地址", max_length=5, choices=builddiingNum)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"收件人"
        verbose_name_plural = u"收件人"


# 员工共有属性


class Employee(BaseInfo):
    employee_id = models.CharField(
        max_length=8, verbose_name="员工id", primary_key=True)

    class Meta:
        abstract = True

# 总仓管理员


class MainWareHouseAdmin(Employee):
    def __str__(self):
        return self.employee_id + " "+self.name

    class Meta:
        verbose_name = u"总仓管理员"
        verbose_name_plural = u"总仓管理员"

# 分仓人员


class WareHouseWorker(Employee):
    level = models.CharField(
        max_length=2, verbose_name="职工类别", choices=workerLevel)
    building = models.CharField(
        verbose_name="负责的楼宇", max_length=5, choices=builddiingNum)

    def __str__(self):
        return self.employee_id + " "+self.name

    class Meta:
        verbose_name = u"分仓人员"
        verbose_name_plural = u"分仓人员"
