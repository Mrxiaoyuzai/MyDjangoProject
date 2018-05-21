"""
Definition of models.
"""

from django.db import models



class MailMessage(models.Model):
    #提醒信息表
    type =models.CharField(max_length=500,verbose_name="类别")
    title = models.CharField(max_length=500,verbose_name="项目描述")
    supplier = models.CharField(max_length=500,verbose_name="供应商",null=True, blank=True)
    message = models.CharField(max_length=4000,verbose_name="提醒内容")
    username = models.CharField(max_length=500,verbose_name="用户名")
    usertitle = models.CharField(max_length=500,verbose_name="负责人",null=True, blank=True)
    useremail = models.CharField(max_length=1000,verbose_name="用户Email",null=True, blank=True)
    remark = models.CharField(max_length=4000,verbose_name="备注",null=True, blank=True)      
    startdate = models.DateTimeField(verbose_name="项目开始日期")
    enddate = models.DateTimeField(verbose_name="项目结束日期")
    sendtime = models.DateTimeField(verbose_name="提醒日期")
    creator = models.CharField(max_length=500,verbose_name="创建人")
    createtime = models.DateTimeField()
    