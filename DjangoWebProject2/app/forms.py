"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm 
from app.models import MailMessage
from django.forms import widgets as Fwidgets
from django.forms import fields as Ffields

TYPE_CHOICES = (('', '--请选择--'),
    ('联动价格更新', '联动价格更新'),
    ('合同到期', '合同到期'),
    ('返利到期追踪', '返利到期追踪'),
    ('设备分期付款', '设备分期付款'),
    ('国产化进度更新', '国产化进度更新'),
    ('日常项目更新', '日常项目更新'),)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class MailMessageForm(ModelForm):
    class Meta:
        model = MailMessage  # 根据 Author 模型创建表单
        #fields = "__all__"
        widgets = {
            'type': Fwidgets.Select(attrs={'class': 'form-control'},choices=TYPE_CHOICES),
            'usertitle':Fwidgets.Select(attrs={'class': 'form-control'},choices=TYPE_CHOICES),
            'title': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'supplier': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'message': Fwidgets.Textarea(attrs={'class': 'form-control'}),
            'message': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'startdate': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'enddate': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'sendtime': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'remark': Fwidgets.Textarea(attrs={'class': 'form-control'}),  
            
            #'username':Fwidgets.HiddenInput(),
        }
        field_classes = {  # 定义字段的类是什么
            #'startdate': Ffields.DateField, # 这里只能填类，加上括号就是对象了。
              #'enddate': Ffields.DateField,
                #'sendtime': Ffields.DateField,
        }
        fields = ['type','usertitle', 'title', 'supplier', 'message','message','startdate', 'enddate','sendtime','remark']  # 该表单包含的字段
