"""
Definition of models.
"""

from django.db import models


class MailMessage(models.Model):
    #提醒信息表
    type =models.CharField(max_length=500,verbose_name="类别",null=True, blank=True)
    title = models.CharField(max_length=500)
    supplier = models.CharField(max_length=500,verbose_name="供应商",null=True, blank=True)
    message = models.CharField(max_length=4000,verbose_name="创建人",null=True, blank=True)
    username = models.CharField(max_length=500,verbose_name="用户名",null=True, blank=True)
    usertitle = models.CharField(max_length=500,verbose_name="用户姓名",null=True, blank=True)
    useremail = models.CharField(max_length=1000,verbose_name="用户Email",null=True, blank=True)
    remark = models.CharField(max_length=4000,verbose_name="备注",null=True, blank=True)      
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    sendtime = models.DateTimeField()
    creator = models.CharField(max_length=500,verbose_name="创建人")
    createtime = models.DateTimeField()
    