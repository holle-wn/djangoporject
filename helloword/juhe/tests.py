import random

from django.test import TestCase
import django
import os

# myfirstproj为你自己的项目名
os.environ['DJANGO_SETTINGS_MODULE'] = 'helloword.settings'
django.setup()
# Create your tests here.
# import datetime
#
# print(datetime.datetime.now())
from django.db.models import Value
from django.db.models.functions import Concat
from juhe.models import User1


def ranstr(length):
    CHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(CHS)
    return salt


def add_one():
    # 添加用户 第一种方法
    user = User1(openid='testl', nickname='test_nick')
    user.save()
    # 第二种
    User1.objects.create(openid='testll', nickname='test_nn')


# add_one()

def add_butch():
    new_users = []
    for i in range(10):
        openid = ranstr(10)
        nickname = ranstr(5)
        user = User1(openid=openid, nickname=nickname)
        new_users.append(user)
    # bulk_create  批量添加数据
    User1.objects.bulk_create(new_users)


# add_butch()

def get_one():
    # 查询一条数据 如果没有则报错
    user = User1.objects.get(openid='testl')
    print(user, user.openid, user.nickname)


# get_one()
def get_filter():
    # 过滤数据  要查询的字段后面加 __
    # contains   查询包含 xxx 的数据
    # users = User1.objects.filter(openid__contains='test')
    # gt  大于 xx 的数据
    # lt  小于 xx 的数据
    # gte  大于等于  lte 小于等于
    users = User1.objects.filter(id__gt=4)

    print(users)


# get_filter()


def get_chain():
    users = User1.objects.filter(openid__contains='test').order_by('openid')
    print(users)


# get_chain()

def modify_one():
    # 更改数据
    user = User1.objects.get(openid='testl')
    user.nickname = 'new_test_nick'
    user.save()


# modify_one()
