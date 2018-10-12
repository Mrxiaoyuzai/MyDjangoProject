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

import base64
from Crypto.Cipher import AES

from app.WSHelper import *

def getCurrentUserName(request):
    username = request.COOKIES.get('PersonalGuid',None)
    if username:
        aes = getAESHelper()  # 初始化加密器
        text_decrypted = str(aes.decrypt(base64.decodebytes(bytes(username, encoding='utf8'))).rstrip(b'\0').rstrip(b'\1').decode("utf8"))
        return text_decrypted
    return None
def getCurrentUser(request):
    currentUser = None
    username = request.COOKIES.get('PersonalGuid',None)
    if username:
        aes = getAESHelper()  # 初始化加密器
        text_decrypted = str(aes.decrypt(base64.decodebytes(bytes(username, encoding='utf8'))).rstrip(b'\0').rstrip(b'\1').decode("utf8"))
        currentUser = getUserInfo(text_decrypted)
    return currentUser
def getChildrenUser(request):
    childList = None
    username = request.COOKIES.get('PersonalGuid',None)
    if username:
        aes = getAESHelper()  # 初始化加密器
        text_decrypted = str(aes.decrypt(base64.decodebytes(bytes(username, encoding='utf8'))).rstrip(b'\0').rstrip(b'\1').decode("utf8"))
        currentUser = getUserInfo(text_decrypted)
        currentUserEntity = currentUser[0][0]
        if currentUserEntity.IsManagementPosition == 1:
            childList = getChildrenUserInfo(currentUserEntity.ADAccount)
        else:
            childList = currentUser[0]
    if(childList):       
        r = [('', '--请选择--')]
        for obj in childList:
           r = r + [(obj.ADAccount, obj.FullName)]
        return r
    #return (('test1','test11'),('test2','test22'))
    return childList

# str不是16的倍数那就补足为16的倍数
def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes
def getAESHelper():
    key = 'ae125efkk4454eef'  # 密码
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
    return aes
def setUserCookie(request):  
    retPrm = request.GET.get('jalsdj')
    #retPrm='hI5PZ2JQC/ct+gJcnPFAzA=='
    if retPrm: #如果获取到域账号
        retPrm = retPrm.replace(' ','+')
       
        aes = getAESHelper()  # 初始化加密器
        '''
        encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16('MASTDOM\cn4062d'))), encoding='utf8').replace('\n', '')  # 加密
        text_decrypted111 = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
        '''
        text_decrypted = str(aes.decrypt(base64.decodebytes(bytes(retPrm, encoding='utf8'))).rstrip(b'\0').rstrip(b'\1').decode("utf8"))  # 解密 多加一个 rstrip(b'\1') 因为C#加密多一个，原因未知
        response = HttpResponseRedirect('http://' + request.get_host() + request.path)
        response.set_cookie('PersonalGuid','bbb' + retPrm)  ###为浏览器回写cookie！！key为username 对应的value为xxx。
        return response
    else:
        myurl = 'http://' + request.get_host() + request.path + '&IsFromPython=1'
        return  HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=' + myurl)
    #return
    #HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=https://www.cnblogs.com/shenh/p/8028081.html')
    #return
    #HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=http://127.0.0.1:8000/list')
def checkIsLogin(request):   
    username = request.COOKIES.get('PersonalGuid',None) #request.session.get('username',None)
    #print(username)
    if username:        
        return True
    else:#没有获取到域账号
        return False
       
def doAction(request):
    if request.method == "GET":
        #print("it's a test") #用于测试
        action = request.GET.get('action') 
        if action == "getList":
            offset = request.GET.get("offset",1)
            limit = request.GET.get("limit",10)
            #message_list =
            #models.MailMessage.objects.all().order_by("-createtime")

            message_list = models.MailMessage.objects.filter(creator__icontains="system").order_by("-createtime")
            
            message_list_json = serializers.serialize("json", message_list)
            
            #print(message_list)
            #json_str = '['
            #for message in message_list:
            #    json_str+='{"id":"' + str(message.id) + '",'
            #    json_str+='"title":"' + str(message.title) + '",'
            #    json_str+='"usertitle":"' + str(message.usertitle) + '",'
            #    json_str+='"supplier":"' + str(message.supplier) + '",'
            #    json_str+='"startdate":"' +
            #    str(message.startdate.strftime("%Y/%m/%d")) + '",'
            #    json_str+='"enddate":"' +
            #    str(message.enddate.strftime("%Y/%m/%d")) + '",'
            #    json_str+='"sendtime":"' +
            #    str(message.sendtime.strftime("%Y/%m/%d")) + '"},'
            #json_str = json_str.rstrip(',')
            #json_str+=']'
            return HttpResponse((message_list_json))
        elif action == "delInfo":
            ids = request.GET.get("checkedRequestID").split('|')
            ids = filter(None, ids)
            mmodel = models.MailMessage.objects.get(id__in=ids).delete()
            return HttpResponse(json.dumps({"result":"ok"}))
        elif action == "detail":
            mid = int(request.POST.get("id",0))
            mmodel = None   
            if(mid > 0):
                mmodel = models.MailMessage.objects.get(id=mid)
            abc = request.GET.get('title',None)
            obj = forms.MailMessageForm(request.GET,instance = mmodel)
            obj.fields['username'].choices = getChildrenUser(request)
            if  obj.is_valid():
                current_time = datetime.now()
                temp = obj.save(commit=False) #commit暂时获取一个数据库对象，对其他字段进行赋值
                if(mid == 0):
                    temp.createtime = current_time
                    temp.creator = getCurrentUserName(request)
                obj.save()
                return HttpResponse(json.dumps({"result":"ok"}))
            else:
                return HttpResponse(json.dumps({"result":"error"}))
        #message_list_json = serializers.serialize("json", message_list)
        #return HttpResponse(message_list_json)
        '''return HttpResponse(json.dumps([{
            "username": "aaa",
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


def list(request):
    """Renders the home page."""
    #print("StartList")
    assert isinstance(request, HttpRequest)
    if not checkIsLogin(request):
       return setUserCookie(request)
    return render(request,
        'app/list.html',
        {
            'title':'list',
            'year':datetime.now().year,
        })


def messageDetail(request):   
    if not checkIsLogin(request):
        return setUserCookie(request)    
    context = {}

    #temp = getChildrenUser(request)

    mid = int(request.GET.get("id",0))
    mmodel = None  
    if mid > 0:
        mmodel = models.MailMessage.objects.get(id=mid)
    obj = forms.MailMessageForm(instance = mmodel)     
   
    obj.fields['username'].choices = getChildrenUser(request)
    #obj.fields['username'].choices = (('321', '--312--'),)
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
