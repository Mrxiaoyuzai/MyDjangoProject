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
        elif action == "getModel":
             id = request.GET.get("id")
             message_model = models.MailMessage.objects.all().order_by("-createtime")
       
       
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

def list(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)    
    return render(request,
        'app/list.html',
        {
            'title':'list',
            'year':datetime.now().year,
        })

def messageDetail(request):
    return render(request,
        'app/MessageDetail.html',
        {
            'title':'Detail',
            'message':'Detail Page.',
            'year':datetime.now().year,
            'mid':'1',
            'mtitle':'mytesttitle',
        })

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
            'title':'About111',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
