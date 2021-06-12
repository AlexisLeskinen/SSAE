import random
from typing import List, Set
from faker import Faker
from backend.models import buildings


class DataGenerator(object):
    cfacker = Faker('zh_CN')
    sexoption = "男女"
    maxNum = 500
    shelves = set()

    def baseinfo(self, number: int) -> List:
        """
        @description: 
        随机生成基础人物信息
        ---------
        @param: 生成数量
        -------
        @Returns: json数组
        -------
        """
        number = number % self.maxNum
        res = []
        for _ in range(number):
            b = {
                'name': self.cfacker.name(),
                'sex': self.sexoption[random.randrange(0, 2)],
                'phone': self.cfacker.phone_number(),
                'building': buildings[random.randrange(1, 13)][0],
                'password': "0000"
            }
            res.append(b)
        return res

    def receiver(self, number: int) -> List:
        """
        @description: 
        随机生成收件人信息
        ---------
        @param: number，生成的数量
        -------
        @Returns: json数组
        -------
        """
        number = number % self.maxNum
        res = self.baseinfo(number)
        for r in res:
            t = {
                'receive_id': str(random.randrange(1, 100000)).zfill(5),
                'self_service': random.randrange(0, 2),
                'door': str(random.randrange(1, 10000)).zfill(4)
            }
            r.update(t)

        return res

    def woker(self, number: int) -> List:
        """
        @description: 
        随机生成工作人员信息
        ---------
        @param: 生成数量
        -------
        @Returns: json数组
        -------
        """
        number = number % self.maxNum
        res = self.baseinfo(number)

        for r in res:
            t = {
                'employee_id': str(random.randrange(1, 100000)).zfill(5),
                'level': random.randrange(1, 3)
            }
            r.update(t)

        return res

    def express(self, number: int) -> List:
        """
        @description: 
        随机生成快递信息，注意要现有收件人信息
        ---------
        @param: 生成数量
        -------
        @Returns: json数组
        -------
        """
        number = number % self.maxNum
        res = []

        for _ in range(number):
            n = random.randrange(0, 2)
            d = 0
            if(n):
                d = random.randrange(0, 2)
            e = {
                'express_id': str(random.randrange(1, 10000000)).zfill(7),
                'is_notified': n,
                'is_divided': d
            }

            res.append(e)

        return res

    def shelf(self) -> str:
        res = ""
        alp = ['A', 'B', 'C', 'D']
        res += alp[random.randint(0, 3)]
        num = str(random.randint(0, 999999)).zfill(6)
        res += num[0] + '-' + num[1] + '-' + num[2::]

        if res in self.shelves:
            res = self.shelf()
        else:
            self.shelves.add(res)

        return res


G = DataGenerator()
