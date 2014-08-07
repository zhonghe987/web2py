# -*- coding: utf-8 -*-
import socket
localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
def interface_API():
    data = ['tagCount','data','count','noTagCount','infos']
    f = dict(breadcrumb=['API文档'],panelTitle='API调用方法',data= data)
    return f

def method_api():
    f = dict(breadcrumb=['API文档'])
    if request.vars.name == "data":
        f['panelTitle']='data API调用方法'
        f['inter']='用于获取所有的数据'
        f['url'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/data?'%(localIP)
        f['args']='name=age'
        f['format']= '参数的数据格式为： k1=v1 '
        f['https'] ='get'
        f['example'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/data?name=age'%(localIP)
        f['json']={"msg": "", "data":[], "errcode": 0, "ret": 0}
        f['args_name']='标签工程的名称'
        return f
    elif request.vars.name == "count":
        f['panelTitle']='count API调用方法'
        f['inter']='用于获取所有的cookie量'
        f['url'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/count?'%(localIP)
        f['args']='name=age'
        f['format']= '参数的数据格式为： k1=v1 '
        f['https'] ='get'
        f['example']='http://%s:8000/LinkDataAdmin/api/tagProj/count?name=age'%(localIP)
        f['args_name']='标签工程的名称'
        f['json']={"msg": "", "data": {"count": 49866, "act": "count"}, "errcode": 0, "ret": 0}
        return f
    elif request.vars.name == "tagCount":
        f['panelTitle']='tagCount API调用方法'
        f['inter']='用于获取已标记的cookie量'
        f['url'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/tagCount?'%(localIP)
        f['args']='name=age'
        f['format']= '参数的数据格式为： k1=v1 '
        f['https'] ='get'
        f['example'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/tagCount?name=age'%(localIP)
        f['args_name']='标签工程的名称'
        f['json']={"msg": "", "data": {"count": 7, "act": "tagCount"}, "errcode": 0, "ret": 0}
        return f
    elif request.vars.name == "noTagCount":
        f['panelTitle']='noTagCount API调用方法'
        f['inter']='用于获取未标记的cookie量'
        f['url'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/noTagCount?'%(localIP)
        f['args']='name=age'
        f['format']='参数的数据格式为： k1=v1 '
        f['example']='http://%s:8000/LinkDataAdmin/api/tagProj/noTagCount?name=age'%(localIP)
        f['https'] ='get'
        f['args_name']='标签工程的名称'
        f['json']={"msg": "", "data": {"count": 49859, "act": "noTagCount"}, "errcode": 0, "ret": 0}
        return f
    elif request.vars.name == "infos":
        f['panelTitle']='infos API调用方法'
        f['inter']='获取数据的信息'
        f['url'] = 'http://%s:8000/LinkDataAdmin/api/tagProj/infos?'%(localIP)
        f['args']='name=age'
        f['format']= '参数的数据格式为： k1=v1 '
        f['https'] ='get'
        f['example']='http://%s:8000/LinkDataAdmin/api/tagProj/infos?name=age'%(localIP)
        f['json']={"msg": "", "data": [{"cookieDomain": "www.qq.com", "dataSourceName": "qq", "createDate": "2014-05-26 10:28:48", "name": "age"}, {"cookieDomain": "www.qq.com", "dataSourceName": "qq", "createDate": "2014-05-27 10:22:48", "name": "age"}, {"cookieDomain": "www.qq.com", "dataSourceName": "qq", "createDate": "2014-05-27 10:18:34", "name": "address"}, {"cookieDomain": "www.qq.com", "dataSourceName": "qq", "createDate": "2014-05-27 10:18:30", "name": "year"}], "errcode": 0, "ret": 0}
        f['args_name']='标签工程的名称'
        return f
    
    
    
    
    return f
    