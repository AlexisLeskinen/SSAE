from django.db import models

# Create your models here.

# 暨大总仓库


class MianWarehouse(models.Model):
    express_id = models.PositiveIntegerField(primary_key=True)
    building = models.CharField(max_length=50)
    receiver = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.express_id

# 楼宇分仓


class MinorWarehouse(models.Model):
    express_id = models.PositiveIntegerField(primary_key=True)
