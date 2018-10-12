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
            'type': Fwidgets.Select(attrs={'class': 'form-control'}),
            'username':Fwidgets.Select(attrs={'class': 'form-control'}),
            'title': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'supplier': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'message': Fwidgets.Textarea(attrs={'class': 'form-control'}),
            'message': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'startdate': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'enddate': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'sendtime': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'remark': Fwidgets.Textarea(attrs={'class': 'form-control'}),  
            'useremail':Fwidgets.HiddenInput(),
            'usertitle':Fwidgets.HiddenInput(),
            #'username':Fwidgets.HiddenInput(),
        }
        field_classes = {  # 定义字段的类是什么
            #'startdate': Ffields.DateField, # 这里只能填类，加上括号就是对象了。
              #'enddate': Ffields.DateField,
                #'sendtime': Ffields.DateField,
        }
        fields = ['type','username', 'title', 'supplier', 'message','message','startdate', 'enddate','sendtime','remark','useremail','usertitle']  # 该表单包含的字段
    username = forms.ChoiceField(label=u'负责人',widget=Fwidgets.Select(attrs={'class': 'form-control'}))
   
    def __init__(self,*args,**kwargs):
        super(MailMessageForm,self).__init__(*args,**kwargs)
        self.fields['username'].choices = (('112', '--请选择--'),)
