from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model): # 主要储存个性化设置和本系统额外权限
    uuid = models.AutoField(primary_key=True)

    login_user_link = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='userinfo',
        default=None,
        null=True
    )

    user_id = models.CharField(max_length=450, unique=True, blank=True,
                                   null=True)
    # 默认00001 分别代表 全局/地区/部门/组/个人 0=只读 1=可写 转化为int储存 使用时解码使用位运算
    auth_condition = models.IntegerField(db_column='auth_condition', default=1)
    personal_settings = models.JSONField(default=dict)
    enabled = models.BooleanField(default=True) # 是否生效
    comment = models.CharField(max_length=450, blank=True, null=True)
    update_time = models.DateTimeField(db_column='updateTime', auto_now=True)
    create_time = models.DateTimeField(db_column='createTime', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'UserInfo'

class Sentence(models.Model):
    uuid = models.AutoField(primary_key=True)
    sentence_content = models.TextField(blank=True,null=True,default='')
    role_choices = [
        (1, 'ai'),
        (2, 'local')
    ]
    role = models.IntegerField(blank=True, null=True, default=1,choices=role_choices)
    enabled = models.BooleanField(default=True)  # 是否生效
    update_time = models.DateTimeField(db_column='updateTime', auto_now=True)
    create_time = models.DateTimeField(db_column='createTime', auto_now_add=True)


class Conversation(models.Model):
    uuid = models.AutoField(primary_key=True)
    user_link = models.ForeignKey('UserInfo', null=True, default=None, on_delete=models.SET_NULL)  # linked user
    label = models.TextField(blank=True,null=True,default='')

    sentence_scope = models.ManyToManyField(Sentence, blank=True)
    enabled = models.BooleanField(default=True)  # 是否生效
    update_time = models.DateTimeField(db_column='updateTime', auto_now=True)
    create_time = models.DateTimeField(db_column='createTime', auto_now_add=True)