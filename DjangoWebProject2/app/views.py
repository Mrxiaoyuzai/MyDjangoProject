"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app import forms
from django.shortcuts import HttpResponse
import json
from app import models
from django.core import serializers
import time
from django.http import HttpResponseRedirect

def checkUser(func):
    def returned_wrapper(request,*arg,**kwargs):
        ret = func(request,*arg,**kwargs)
        return ret
        username =request.COOKIES.get('username',None) #request.session.get('username',None)
        if username:
            ret = func(request,*arg,**kwargs)
            return ret
        else:
            #return HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=https://www.cnblogs.com/shenh/p/8028081.html')
            return HttpResponseRedirect('about')
    return returned_wrapper



def doAction(request):
    if request.method == "GET":
        print("it's a test")     #用于测试
        action = request.GET.get('action') 
        if action == "getList":
            offset = request.GET.get("offset",1)
            limit = request.GET.get("limit",10)
            message_list = models.MailMessage.objects.all().order_by("-createtime")
            #message_list_json = serializers.serialize("json", message_list)
            json_str = '['
            for message in message_list:
                json_str+='{"id":"' + str(message.id) + '",'
                json_str+='"title":"' + str(message.title) + '",'
                json_str+='"usertitle":"' + str(message.usertitle) + '",'
                json_str+='"supplier":"' + str(message.supplier) + '",'
                json_str+='"startdate":"' + str(message.startdate.strftime("%Y/%m/%d")) + '",'
                json_str+='"enddate":"' + str(message.enddate.strftime("%Y/%m/%d")) + '",'
                json_str+='"sendtime":"' + str(message.sendtime.strftime("%Y/%m/%d")) + '"},'
            json_str = json_str.rstrip(',')
            json_str+=']'
            return HttpResponse((json_str))
        elif action == "delInfo":
            ids = request.GET.get("checkedRequestID").split('|')
            ids = filter(None, ids)
            mmodel = models.MailMessage.objects.get(id__in=ids).delete()
            return HttpResponse(json.dumps({"result":"ok"}))
       
        #message_list_json = serializers.serialize("json", message_list)
        #return HttpResponse(message_list_json)
        '''return HttpResponse(json.dumps([{
            "usertitle": "aaa",
            "title": "bbb",          
        }]))'''
    else:
        name = request.GET.get('action') 
        gid = request.GET.get('groupid') 
        status = name
        result = gid
        return HttpResponse(json.dumps({
            "status": status,
            "result": result,          
        }))

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)    
    return render(request,
        'app/index.html',
        {
            'title':'Home Page My Test',
            'year':datetime.now().year,
        })
@checkUser
def list(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)    
    return render(request,
        'app/list.html',
        {
            'title':'list',
            'year':datetime.now().year,
        })
def getUserSelect():
    return (('test1','test11'),('test2','test22'))

@checkUser
def messageDetail(request):
    
    context = {}
    mid = int(request.GET.get("id",0))
    mmodel = None
    if(mid > 0):
        mmodel = models.MailMessage.objects.get(id=mid)
    
    if request.method == "POST":
        obj = forms.MailMessageForm(request.POST,instance = mmodel)
        if obj.is_valid():
            current_time = datetime.now()
            temp = obj.save(commit=False) #commit暂时获取一个数据库对象，对其他字段进行赋值
            temp.createtime = current_time
            temp.creator = 'system'
            obj.save()
            return HttpResponse(json.dumps({"result":"ok"}))
    else:    
        obj = forms.MailMessageForm(instance = mmodel)

    obj.fields['usertitle'].choices = (('test1','test11'),('test2','test22'))
    context['mailemessage_form'] = obj
    return render(request,'app/MessageDetail.html',context)
   

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
