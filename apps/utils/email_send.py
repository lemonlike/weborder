# -*- coding: utf-8 -*-
__author__ = 'lemon'

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from weborder.settings import EMAIL_FROM


def random_str(randomlength=8):
    """
    生成随机字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_email(email, send_type):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = u"在线点餐网激活链接"
        email_body = u"请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == "forget":
        email_title = u"在线点餐网修改密码链接"
        email_body = u"请点击下面链接修改你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

