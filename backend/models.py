from django.db import models

# Create your models here.

# 快递信息


class ExpressInfo(models.Model):
    # id
    express_id = models.PositiveIntegerField(primary_key=True)
    # 建筑号数
    building = models.CharField(max_length=50)
    # 收件人
    receiver = models.CharField(max_length=10)
    # 手机
    phone = models.CharField(max_length=12)
    # 备注
    note = models.TextField()
    # 位置号 （A5-2-2210）
    locate = models.CharField(max_length=15)

    def __str__(self):
        return self.express_id
