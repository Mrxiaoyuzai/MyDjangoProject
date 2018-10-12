class WSHelper(object):
    """description of class"""

import suds
from suds.client import Client

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

