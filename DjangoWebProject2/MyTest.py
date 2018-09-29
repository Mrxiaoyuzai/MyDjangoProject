class MyTest(object):
    """description of class"""

import suds
from suds.client import Client
url = "http://ws.linde-xiamen.com.cn/EHRWebService/EHRWebService.asmx?wsdl"
client = suds.client.Client(url)
result = client.service.GetManagerByEmployeeID(4142,0)
print(client)
#print(result['FullTitle'])
print("11")
input("End")
input("Please intput your name:")

