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
def getChildrenUserInfo(Initial):
    url = "http://ws.linde-xiamen.com.cn/EHRWebService/EHRWebService.asmx?wsdl"
    client = suds.client.Client(url)
    dynaticondition = ' (!IsDeleted.HasValue or IsDeleted.Value==0) and Initial=="' + Initial + '"'
    result = client.service.GetEmployeesByDynamic(dynaticondition)
    #print(client)
    return result

def handleMessageMail(currentUrl=''):
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
                sendUrl = ''
                if currentUrl:
                    sendUrl = '。<a href="' + currentUrl + '">查看</a>'
                content+= sendUrl
                result = client.service.SendMail(entity.useremail,'',subject,content,None,'')

                res = entity.useremail + '---' + subject + '---' + content
                models.MailLog.objects.create(mid=entity.id,result=res,createtime=timenow)
        except Exception as e:
                models.MailLog.objects.create(mid=entity.id,result=repr(e),createtime=timenow)
    #print(client)
    return result


from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
 

class cxlEncoder(object):
    def __init__(self, key):
       self.key = key.encode('utf-8')
       self.mode = AES.MODE_ECB    
    def addTo16(self,val):
        while len(val) % 16 != 0:
            val += '\0'
        return str.encode(val)  # 返回bytes
    def encrypt(self, text):
        cryptor = AES.new(self.key,self.mode)
        encrypted_text = str(base64.encodebytes(cryptor.encrypt(self.addTo16(text))), encoding='utf8').replace('\n', '')
        return encrypted_text

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode)
        text_decrypted = str(cryptor.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).rstrip(b'\0').rstrip(b'\1').rstrip(b'\2').decode("utf8")) 
        return text_decrypted
class PrpCrypt(object): 
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
    
    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
 
    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        # return plain_text.rstrip('\0')
        return bytes.decode(plain_text).rstrip('\0')