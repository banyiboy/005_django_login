# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
from datetime import datetime
from string import printable
from pbkdf2 import PBKDF2
# Create your models here.

class User(models.Model):
    """用户表"""

    #一个char(32)的固定类型，使用时需要导入uuid库。
    uuid =  models.UUIDField(verbose_name=u'uuid', unique=True, default=uuid4)
    name = models.CharField(verbose_name=u'姓名', max_length=50, unique=True)
    _password = models.CharField(verbose_name=u'密码', max_length=128)

    loginnum = models.IntegerField(verbose_name=u'登录次数', default=0)

    last_login = models.DateTimeField(blank=True, null=True)
    createtime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add= True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    _locked = models.BooleanField(verbose_name=u'是否被锁定', default=False)
    _isdelete = models.BooleanField(verbose_name=u'是否被删除', default=False)

    _avatar = models.CharField(verbose_name=u'头像', max_length=128)#头像路径

    email = models.EmailField(verbose_name=u'邮箱')
    mobile = models.CharField(verbose_name=u'手机号', max_length=50)
    qq = models.CharField(verbose_name=u'QQ号', max_length=50)


    @classmethod
    def all(cls):
        return cls.objects.all()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        print self._hash_password(password)
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @property
    def avatar(self):
        return self._avatar if self._avatar else "default_avatar.jpg"


    @avatar.setter
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):
                    os.unlink("static/images/useravatars/" + self._avatar)
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_login': self.last_login,
        }

    def __str__(self):
        return "%s : %s" % (self.id, self.name)


