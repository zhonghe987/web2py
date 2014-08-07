﻿# -*- coding: utf-8 -*-

LIST_NUM = 10

def __getKeyNames(data):
    keyNames = []
    for i in range(1,4):
        k = 'keyname%d' %i
        n = data[k]
        if n:
            keyNames.append('%s:%s' %(n,data['%s_value' %k]))
    return ','.join(keyNames)

@auth.requires_login()
def index():
    #print 'auth', auth.user
    s = [OPTION('全部',_value='all'),OPTION('运行',_value='run'),OPTION('暂停',_value='stop')]
    cookie = [OPTION(c.cookieDomain,_value = c.cookieDomain) for c in lda_db(lda_db.dataSource.account_id == auth.user.id).select(lda_db.dataSource.cookieDomain,groupby=lda_db.dataSource.cookieDomain)] 
    cookie.insert(0,OPTION('全部域名',_value='all_yu'))
    status = SELECT(s,_class="form-control form-input",_id= "status",_name="status")
    cookiedom = SELECT(cookie,_class="form-control form-input",_id="cookiedom",_name="cookiedom")
    cnd = (lda_db.dataSource.account_id==auth.user.id) & (lda_db.dataSource.dsStatus != 'delete')      
    data = lda_db(cnd).select(orderby=lda_db.dataSource.date )
    #count = lda_db(lda_db.dataSource.account_id==auth.user.id).count()
    return dict(data = data, breadcrumb=['数据源管理'], panelTitle='',cookie = cookiedom,status = status)



def sourceFind():
    cnd = (lda_db.dataSource.account_id==auth.user.id) & (lda_db.dataSource.dsStatus != 'delete')
    if request.vars:
        if request.vars.dataSname:
            cnd = cnd & (lda_db.dataSource.dsName.like('%%%s%%' %request.vars.dataSname)) 
        if request.vars.cookiedom !='all_yu':
            cnd = cnd & (lda_db.dataSource.cookieDomain == request.vars.cookiedom)
        if request.vars.status != 'all':
            cnd = cnd & (lda_db.dataSource.dsStatus == request.vars.status)      
    data = lda_db(cnd).select(orderby=lda_db.dataSource.date )
    import gluon.contrib.simplejson
    return response.json(dict(data = data))


@auth.requires_login()
def new():
    import time
    dates = time.strftime('%Y-%m-%d:%H:%M:%S',time.localtime(time.time()))
    btn = INPUT(_value='继续保存',_type='submit',_id='subt')
    form = SQLFORM.factory(
                Field('name',requires=IS_NOT_EMPTY()),
                Field('domain', requires=IS_NOT_EMPTY()),
                Field('keyname1', requires=IS_NOT_EMPTY()),
                Field('keyname1_value', requires=IS_NOT_EMPTY()),
                Field('keyname2'),
                Field('keyname2_value'),
                Field('keyname3'),
                Field('keyname3_value'),   
                buttons = [btn]
                )
    num = lda_db.executesql('select count(d_id) from dataSource where account_id = %s'%(auth.user.id))
    if num[0][0] < 4:
        if request.vars.name and  request.vars.domain:
            keyNames = __getKeyNames(request.vars)
            r = lda_db.dataSource.insert(account_id=auth.user.id, 
                                                                     dsName=request.vars.name,
                                                                     cookieDomain=request.vars.domain,
                                                                     keyNames=keyNames,
                                                                     date = dates)
            tbl = 'DS_%s' %r
            lda_db.executesql('CREATE TABLE %s (ds_id int, cookieId varchar(45), lastDate datetime, primary key (ds_id)) engine=MyISAM DEFAULT CHARSET=utf8' %tbl)
            scheduler.queue_task('updateDS', pvars=dict(table=tbl, cookDomain=request.vars.domain), timeout=86400)
            redirect(URL('dataSource','index'))
        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill the form-> %s' %auth.user

    return dict(form=form,breadcrumb=['数据源管理','新增数据源'], panelTitle='新增数据源')


@auth.requires_login()
def show():
    btn = INPUT(_value='查找',_type='submit',_id='sub')
    form = SQLFORM.factory(Field('firsttime', requires=[IS_NOT_EMPTY(error_message='cannot'),IS_DATE(format=T('%Y-%m-%d'),error_message='must be YYYY-MM-DD!')]),
                           Field('lasttime',requires = [IS_NOT_EMPTY(error_message='cannot'),IS_DATE(format=T('%Y-%m-%d'),error_message='must be YYYY-MM-DD!')]),
                           buttons = [btn]
                          )
    
    
    ks=[]
    data = lda_db(lda_db.dataSource.d_id == request.vars.sh_id).select(lda_db.dataSource.dsName,lda_db.dataSource.cookieDomain,lda_db.dataSource.keyNames).first()
    for ke in data.keyNames.split(','):
        ks.append(ke.split(":"))
    data.keyNames = ks 
    cookCount = lda_db(lda_db.cookieActiveDay.dataSourceId==request.get_vars.sh_id).count()
    import math
    pageCount =  int(math.ceil(cookCount/float(LIST_NUM)))
    cookData = lda_db(lda_db.cookieActiveDay.dataSourceId==request.get_vars.sh_id).select(lda_db.cookieActiveDay.count,lda_db.cookieActiveDay.date, orderby="cid desc", limitby=(0,LIST_NUM))
    return dict(data = data,form=form,home='active',profile='',homes="tab-pane active",profs='tab-pane',breadcrumb=['数据源管理','查看数据源'],panelTitle='',
                          cookData=cookData,cookCount=cookCount,pageCount=pageCount,ds_id=request.get_vars.sh_id)




def  changeDate(dates):
    if dates:
        ds = dates.split('/')
        return '-'.join([ds[2],ds[0],ds[1]])
    return 
    
def  dele():
    if request.vars.de_id:
        lda_db.executesql("update dataSource set dsStatus = 'delete' where d_id=%s"%(request.vars.de_id))
    redirect(URL('dataSource','index'))
    


    
def cookFind():
    cnd = (lda_db.cookieActiveDay.dataSourceId==request.post_vars.dsId)
    if request.post_vars.startDate:
        cnd = cnd & (lda_db.cookieActiveDay.date >= request.post_vars.startDate)
    if request.post_vars.endDate:
        cnd = cnd & (lda_db.cookieActiveDay.date <= request.post_vars.endDate)
    dc = lda_db(cnd).count()
    import math
    pc =  int(math.ceil(dc/float(LIST_NUM)))
    data = lda_db(cnd).select(lda_db.cookieActiveDay.count,lda_db.cookieActiveDay.date, orderby="cid desc", limitby=(0,LIST_NUM))
    import gluon.contrib.simplejson
    return response.json(dict(cookData=data, pageCount=pc, cookCount=dc))
    


def changeStatus():
    from AppFunc import getStatus, getStatusButton
    import json
    #print  'change status post data:',request.post_vars
    if request.post_vars.status == 'run':
        s = 'stop'
    elif request.post_vars.status == 'stop':
        s = 'run'
    lda_db.executesql("update dataSource set dsStatus='%s' where d_id=%s" %(s,request.post_vars.id))
    return json.dumps(dict(status=s, stName=getStatus(s), stButton=getStatusButton(s)))


def lock_batch():
    value = request.post_vars.all_ids
    lda_db.executesql("update  dataSource set dsStatus='delete'  where d_id in  (%s)"%(value[:-1]))
    return 0
    
    
def valit_unique():
    #print [request.post_vars.dataname]
    if lda_db((lda_db.dataSource.account_id==request.post_vars.acc_id) 
                       & (lda_db.dataSource.dsName==request.post_vars.dataname)).select().first():
        return  1
    return 0
        
def cookPaginate():
    print request.post_vars
    sPos = (int(request.post_vars.page) - 1) * LIST_NUM
    cnd = (lda_db.cookieActiveDay.dataSourceId==request.post_vars.dsId)
    if request.post_vars.startDate:
        cnd = cnd & (lda_db.cookieActiveDay.date >= request.post_vars.startDate)
    if request.post_vars.endDate:
        cnd = cnd & (lda_db.cookieActiveDay.date <= request.post_vars.endDate)
    data = lda_db(cnd).select(lda_db.cookieActiveDay.count,lda_db.cookieActiveDay.date, orderby="cid desc", limitby=(sPos,sPos+LIST_NUM)) 
    
    return response.json(dict(cookData=data))


