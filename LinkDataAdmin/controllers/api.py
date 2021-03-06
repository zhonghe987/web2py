# -*- coding: utf-8 -*-

ERROR = ['',
 '用户名或密码不存在',
 '标签项目不存在',
]



def __data(user, **vars):
    errcode = 0
    data = []
    tagProj = lda_db((lda_db.tagProj.account_id==user.id) & (lda_db.tagProj.tpStatus!='delete') & (lda_db.tagProj.tpName==vars['name'])).select().first() 
    if tagProj:
        data = lda_db.executesql("select ds_id,cookieId from Tag_%s" %tagProj.id)
        print 'data', len(data)
        data = []
    else:
        errcode = 2
        
    return errcode, data

def __count(user, **vars):
    errcode = 0
    count = dict(count=0,act='count')
    tagProj = lda_db((lda_db.tagProj.account_id==user.id) & (lda_db.tagProj.tpStatus!='delete') & (lda_db.tagProj.tpName==vars['name'])).select().first() 
    if tagProj:
        data = lda_db.executesql("select count(ds_id) from Tag_%s" %tagProj.id)
        if data:
            count['count'] = data[0][0]
    else:
        errcode = 2
    return errcode, count

def __tagCount(user, **vars):
    errcode = 0
    count = dict(count=0,act='tagCount')
    tagProj = lda_db((lda_db.tagProj.account_id==user.id) & (lda_db.tagProj.tpStatus!='delete') & (lda_db.tagProj.tpName==vars['name'])).select().first() 
    if tagProj:
        data = lda_db.executesql("select count(ds_id) from Tag_%s where ti_id>0" %tagProj.id)
        if data:
            count['count'] = data[0][0]
    else:
        errcode = 2
    return errcode, count

def __noTagCount(user, **vars):
    errcode = 0
    count = dict(count=0,act='noTagCount')
    tagProj = lda_db((lda_db.tagProj.account_id==user.id) & (lda_db.tagProj.tpStatus!='delete') & (lda_db.tagProj.tpName==vars['name'])).select().first() 
    if tagProj:
        data = lda_db.executesql("select count(ds_id) from Tag_%s where ti_id=0" %tagProj.id)
        if data:
            count['count'] = data[0][0]
    else:
        errcode = 2
    return errcode, count

def __infos(user, **vars):
    tagProj = lda_db((lda_db.tagProj.account_id==user.id) & (lda_db.tagProj.tpStatus!='delete')).select(lda_db.tagProj.tpName,lda_db.tagProj.date,
                                                                                                                                                                                                         lda_db.dataSource.dsName,lda_db.dataSource.cookieDomain,
                                                                                                                                                                                                         join=lda_db.dataSource.on(lda_db.tagProj.dataSource_id==lda_db.dataSource.id))
    data = [dict(name=t.tagProj.tpName, createDate=t.tagProj.date, dataSourceName=t.dataSource.dsName, cookieDomain=t.dataSource.cookieDomain) for t in tagProj]
    return 0, data

GET_METHODS = dict(count=__count, tagCount=__tagCount, noTagCount=__noTagCount,
                                          infos=__infos, data=__data, )



@request.restful()
def tagProj():
    print 'api'
    response.view = 'generic.json'
    def GET(act, **vars):
        print act, vars
        errcode, data = GET_METHODS[act](auth.user, **vars)
        return dict(errcode=errcode,msg=ERROR[errcode], ret=errcode or 0,  data=data)
    return locals()