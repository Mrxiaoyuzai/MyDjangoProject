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



from app.WSHelper import *
from django.db.models import Q


encoder = cxlEncoder('ae125efkk4454eef')
def writeLog(str):
    try:
        f = open('log/log.txt', 'a+') # 若是'wb'就表示写二进制文件
        f.writelines(str + '\n')
    except:
         f.writelines('Write to log error\n')
    finally:
        f.close()

def getCurrentUserName(request):
    username = request.COOKIES.get('TmpGuid',None)
    if username:        
        text_decrypted = encoder.decrypt(username) 
        return text_decrypted
    return None
def getCurrentUser(request):
    currentUser = None
    username = request.COOKIES.get('TmpGuid',None)
    if username:
        aes = getAESHelper()  # 初始化加密器
        text_decrypted = encoder.decrypt(username)  
        currentUser = getUserInfo(text_decrypted)
    return currentUser
def getChildrenUser(request):
    childList = None
    try:
        username = request.COOKIES.get('TmpGuid',None)
        #username = 'jz92Rz6iqqplcKua72rJ4g=='
        writeLog('CurrentUserEncrpted:' + username)
        if username:          
            text_decrypted = encoder.decrypt(username) 
            writeLog('CurrentUser:' + text_decrypted)
            currentUser = getUserInfo(text_decrypted)
            writeLog('CurrentUser:' + str(currentUser))
            currentUserEntity = currentUser[0][0]
            if currentUserEntity.IsManagementPosition == 1:
                childList = getChildrenUserInfo(currentUserEntity.Initial)[0]
            else:
                childList = currentUser[0]
        if(childList):       
            r = [('', '--请选择--')]
            for obj in childList:
               r = r + [(obj.ADAccount, obj.FullName)]
            return r
    except Exception as e:
        writeLog(repr(e))
    #return (('test1','test11'),('test2','test22'))
    return childList


def setUserCookie(request):  
    retPrm = request.GET.get('jalsdj')
    #retPrm='hI5PZ2JQC/ct+gJcnPFAzA=='
    if retPrm: #如果获取到域账号
        retPrm = retPrm.replace(' ','+')     

        text_decrypted =  encoder.decrypt(retPrm) 
        response = HttpResponseRedirect('http://' + request.get_host() + request.path)
        response.set_cookie('TmpGuid', retPrm)  ###为浏览器回写cookie！！key为username 对应的value为xxx。
        return response
    else:
        myurl = 'http://' + request.get_host() + request.path + '&IsFromPython=1'
        return  HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=' + myurl)
    #return
    #HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=https://www.cnblogs.com/shenh/p/8028081.html')
    #return
    #HttpResponseRedirect('http://webapps.linde-xiamen.com.cn/VerifyIdentity2Java/SkipPage.aspx?myurl=http://127.0.0.1:8000/list')
def checkIsLogin(request):   
    username = request.COOKIES.get('TmpGuid',None) #request.session.get('username',None)
    #print(username)
    if username:        
        return True
    else:#没有获取到域账号
        return False
       
def doAction(request):
    if request.method == "GET":
        #print("it's a test") #用于测试
        action = request.GET.get('action')
        if action == "handleSendingTask":
            handleMessageMail('http://' + request.get_host() + request.path.replace('doAction','list'))#获取调用url 替换doAction 为list
            return HttpResponse(json.dumps({"result":"ok"}))
        if action == "getList":
            offset = request.GET.get("offset",1)
            limit = request.GET.get("limit",10)
           
            #models.MailMessage.objects.all().order_by("-createtime")
            un = getCurrentUserName(request)
            message_list = models.MailMessage.objects.filter(Q(creator__icontains=un) | Q(username__icontains = un)).order_by("-createtime")
            
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
            #ids = filter(None, ids)
            mmodel = models.MailMessage.objects.filter(id__in=ids).delete()
            return HttpResponse(json.dumps({"result":"ok"}))
        elif action == "detail":
            mid = int(request.GET.get("hdID",0))
            mmodel = None   
            if(mid > 0):
                mmodel = models.MailMessage.objects.get(id=mid)            
            obj = forms.MailMessageForm(request.GET,instance = mmodel)
            obj.fields['username'].choices = getChildrenUser(request)
            if  obj.is_valid():
                current_time = datetime.now()
                temp = obj.save(commit=False) #commit暂时获取一个数据库对象，对其他字段进行赋值
                uinfo = getUserInfo(temp.username)[0][0]
                temp.usertitle = uinfo.FullName
                temp.useremail = uinfo.Email
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
    #handleMessageMail()
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
    tmp = request.GET.get('tmp') 
   

  
    pc = PrpCrypt('ae125efkk4454eef')      #初始化密钥
    e = pc.encrypt("MASTDOM\cn40F7")
    d = pc.decrypt(e)     



    encoder = cxlEncoder('ae125efkk4454eef')
    tt = encoder.encrypt('MASTDOM\cn40F7')
    t2 = encoder.decrypt('jz92Rz6iqqplcKua72rJ4g==')
    return render(request,
        'app/list.html',
        {
            'title':'合同到期提醒',
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
    context['mid'] = mid
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
