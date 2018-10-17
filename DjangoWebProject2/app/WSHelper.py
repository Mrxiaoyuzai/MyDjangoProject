class WSHelper(object):
    """description of class"""

import suds
from suds.client import Client
from app import models
from django.utils import timezone

def getUserInfo(ADAccount):

    url = "http://ws.linde-xiamen.com.cn/EHRWebService/EHRWebService.asmx?wsdl"
    client = suds.client.Client(url)
    dynaticondition = ' (!IsDeleted.HasValue or IsDeleted.Value==0) and adaccount.Contains("' + ADAccount + '")'
    result = client.service.GetEmployeesByDynamic(dynaticondition)
    #print(client)
    return result
    #print(result['FullTitle'])
def getChildrenUserInfo(currentUser):
    url = "http://ws.linde-xiamen.com.cn/EHRWebService/EHRWebService.asmx?wsdl"
    client = suds.client.Client(url)
    dynaticondition = ' (!IsDeleted.HasValue or IsDeleted.Value==0) and adaccount.Contains("' + ADAccount + '")'
    result = client.service.GetEmployeesByDynamic(dynaticondition)
    #print(client)
    return result

def handleMessageMail():
    url = 'http://ws.linde-xiamen.com.cn/CommonWebService/MailHelper.asmx?wsdl'
    client = suds.client.Client(url)
    result = None
    timenow = timezone.now()
    message_list = models.MailMessage.objects.filter(sendtime=timenow.date()).order_by("-createtime")
    for entity in message_list:
        try:
            if entity.useremail:
                subject = '[' + entity.title + ']项目到期提醒'
                content = entity.usertitle + ':<br />' + '&nbsp;&nbsp;&nbsp;&nbsp;你的"' + entity.title + '"即将到期，请处理，项目结束日期：' + entity.enddate.strftime("%Y-%m-%d") 
                result = client.service.SendMail(entity.useremail,'',subject,content,None,'')

                res = entity.useremail + '---' + subject + '---' + content
                models.MailLog.objects.create(mid=entity.id,result=res,createtime=timenow)
        except Exception as e:
                models.MailLog.objects.create(mid=entity.id,result=repr(e),createtime=timenow)
    #print(client)
    return result

