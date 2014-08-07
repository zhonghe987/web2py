# -*- coding: utf-8 -*-

LIST_NUM = 10

@auth.requires_login()
def index():
    s = [('all','全部')]
    s.extend([(d.id,'%s (%s)' %(d.dsName,d.cookieDomain)) for d in lda_db(lda_db.dataSource.account_id == auth.user.id).select()])
    btn = INPUT(_value='搜索',_type='submit',_id='sub')
    form = SQLFORM.factory(Field('name'),
                                                      Field('source',requires=IS_IN_SET(s)),
                                                      buttons = [btn]
                                                     ) 
    form.accepts(request, session)
    data = lda_db((lda_db.tagProj.account_id==auth.user.id) & (lda_db.tagProj.tpStatus!='delete')).select(lda_db.tagProj.id,lda_db.tagProj.tpName,lda_db.tagProj.tpStatus,lda_db.tagProj.date,
                                                                                                                            lda_db.dataSource.dsName,lda_db.dataSource.cookieDomain,lda_db.dataSource.id,
                                                                                                                            join=lda_db.dataSource.on(lda_db.tagProj.dataSource_id==lda_db.dataSource.id))
    return dict(form=form, data=data, breadcrumb=['标签项目管理'], panelTitle='标签项目管理' )

@auth.requires_login()
def new():
    
    dataSource = lda_db(lda_db.dataSource.account_id==auth.user.id).select()
    options = [(ds.id, '%s (%s)' %(ds.dsName,ds.cookieDomain)) for ds in dataSource]
    btn_sub = INPUT(_type='submit', _value='保存',_id='sub')
    btn_cnl = INPUT(_value='取消', _type='button', _id='cancel')
    form = SQLFORM.factory(Field('name', requires=IS_NOT_EMPTY()),
                                                      Field( 'source', requires = IS_IN_SET(options)),
                                                      buttons = [btn_sub, btn_cnl]
                )
    num = lda_db.executesql('select count(tp_id) from tagProj where account_id = %s'%(auth.user.id))
    if num[0][0] < 4:
        import time
        dates = time.strftime('%Y-%m-%d:%H:%M:%S',time.localtime(time.time()))
        if form.accepts(request, session):
            r = lda_db.tagProj.insert(account_id=auth.user.id, dataSource_id=form.vars.source, tpName=form.vars.name,date = dates)
            lda_db.executesql("CREATE TABLE Tag_%s (ds_id int, ti_id int DEFAULT '0', cookieId varchar(45), primary key (ds_id)) engine=MyISAM DEFAULT CHARSET=utf8" %r)
            lda_db.executesql('CREATE TABLE TagItem_%s (ti_id int, count int, value varchar(45), date datetime, primary key (ti_id)) engine=MyISAM DEFAULT CHARSET=utf8' %r)
            scheduler.queue_task('dsToTag', pvars=dict(ds='DS_%s' %form.vars.source, tag='Tag_%s' %r), timeout=86400)
            #增加权限
            g_id = auth.id_group(auth.user.company)
            auth.add_permission(g_id,'read','Tag_%s' %r,0)
            auth.add_permission(g_id,'insert', 'Tag_%s' %r, 0)
            auth.add_permission(g_id,'update','Tag_%s' %r, 0)
            auth.add_permission(g_id,'read','TagItem_%s' %r,0)
            auth.add_permission(g_id,'insert', 'TagItem_%s' %r, 0)
            auth.add_permission(g_id,'update','TagItem_%s' %r, 0)
            redirect(URL('index'))
        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill the form -> %s' %options

    return dict(form=form, breadcrumb=['标签项目管理','新增标签项目'], panelTitle='新增标签项目')

@auth.requires_login()
def  editTag():
    s=[request.vars.cookie]
    btn_sub = INPUT(_value='保存',_type='submit',_id='sube')
    btn_cnl = INPUT(_value='取消', _type='button', _id='cancel')
    form = SQLFORM.factory(Field('ed_tagname'),
                                                      Field('source',requires=IS_IN_SET(s)),
                                                      buttons = [btn_sub, btn_cnl]
                  ) 
    
    if form.accepts(request, session):
        lda_db.executesql("update tagProj set tpName = '%s' where tp_id = %s and dataSource_id = %s"%(request.vars.ed_tagname,request.vars.tag_id,request.vars.ds_id))
        redirect(URL('tagProj','index'))
    return dict(form = form,breadcrumb=['标签项目管理','新增标签项目'], panelTitle='编辑标签项目')

def deleTagP():
    lda_db.executesql( "update tagProj set  tpStatus = 'delete'  where tp_id = %s"%request.post_vars.de_id)
    return 0

@auth.requires_login()
def sync():
    dsId = request.vars.dsId
    tpId = request.vars.tpId
    tagProj = lda_db(lda_db.tagProj.id==tpId).select().first()
    session.tagProj = tagProj
    ds = lda_db(lda_db.dataSource.id==dsId).select().first()
    session.dataSource = ds
    #maxId = lda_db.executesql('SELECT max(ds_id) FROM Tag_%s' %tpId)[0][0]
    #if maxId:
    #    lda_db.executesql("INSERT INTO Tag_%s(ds_id,cookieId) SELECT ds_id,cookieId FROM DS_%s WHERE ds_id > %d" %(tpId,dsId,maxId))
    allCount = lda_db.executesql('SELECT count(ds_id) FROM Tag_%s' %tpId)[0][0]
    noCount = lda_db.executesql('SELECT count(ds_id) FROM Tag_%s WHERE ti_id=0' %tpId)[0][0]
    # 历史同步数据
    import math
    dc = lda_db(lda_db.tagSyncLog.tagProjId==tpId).count()
    pc = int(math.ceil(dc/float(LIST_NUM)))
    data = lda_db(lda_db.tagSyncLog.tagProjId==tpId).select(orderby="tid desc", limitby=(0,LIST_NUM))
    return dict(tagProjName=tagProj.tpName, projId=tpId,
                          dataSource='%s (%s)' %(ds.dsName,ds.cookieDomain),
                          counted=allCount-noCount, noCount=noCount,
                           syncData=data.as_json(), pageCount=pc, dataCount=dc,
                           breadcrumb=['标签项目管理','同步标签项'], panelTitle='同步标签项')



def uploadFiles():
    import os.path
    import datetime
    p = os.path.join(request.folder,'uploads')
    fn = os.path.join(p,'%s' %request.vars.name)
    with open(fn,'wb') as f:
        f.write(request.vars.file.value)
    d =  datetime.datetime.now()   
    projId = request.vars.tagProjId
    new = os.path.join(p, '%s-%s.csv' %(projId, d.strftime('%Y%m%d%H%M%S')))
    os.rename(fn, new)
    id = lda_db.tagSyncLog.insert(tagProjId=projId,date=d)
    r = lda_db(lda_db.tagSyncLog.id==id).select().first()
    #print 'fin'
    scheduler.queue_task('updateTagDB', pvars=dict(filename=new, tagProjId=projId, logId=id), timeout=3600)
    return  response.json(dict(logId=id, date=d.date(),row=r))
    

def syncPaginate():
    #print request.post_vars
    sPos = (int(request.post_vars.page) - 1) * LIST_NUM
    tagProjId = request.post_vars.projId
    data = lda_db(lda_db.tagSyncLog.tagProjId==tagProjId).select(orderby="tid desc", limitby=(sPos,sPos+LIST_NUM)) 
    pc = 0
    dc = 0
    if request.post_vars.reCount:
        import math
        dc = lda_db(lda_db.tagSyncLog.tagProjId==tagProjId).count()
        pc = int(math.ceil(dc/float(LIST_NUM)))
    return response.json(dict(syncData=data, dataCount=dc, pageCount=pc))

def projFind():
    s = [('all','全部')]
    s.extend([(d.id,'%s (%s)' %(d.dsName,d.cookieDomain)) for d in lda_db(lda_db.dataSource.account_id == auth.user.id).select()])
    form = SQLFORM.factory(Field('name'),
                                                      Field('source',requires=IS_IN_SET(s))
                                                    )
    cnd = (lda_db.tagProj.account_id==auth.user.id) & (lda_db.tagProj.tpStatus!='delete')
    
    if form.accepts(request.post_vars, session):
        if request.post_vars.name:
            cnd = cnd & (lda_db.tagProj.tpName.like('%%%s%%'%request.post_vars.name))
     
        if request.post_vars.source != 'all':
            cnd = cnd & (lda_db.tagProj.dataSource_id==request.post_vars.source)

    data = lda_db(cnd).select(lda_db.tagProj.id,lda_db.tagProj.tpName,lda_db.tagProj.tpStatus,lda_db.tagProj.date,
                              lda_db.dataSource.dsName,lda_db.dataSource.cookieDomain,lda_db.dataSource.id,
                              join=lda_db.dataSource.on(lda_db.tagProj.dataSource_id==lda_db.dataSource.id))
    return response.json(dict(data=data))



def tagValit():
    tpName = lda_db(lda_db.tagProj.account_id == request.post_vars.uid).select(lda_db.tagProj.tpName) 
    das = [data.tpName for data in tpName]
    if request.post_vars.tname in das:
        return 1
    return 0


def getTaskProgress():
    import datetime
    print 'get task progress:', request.post_vars
    d = sch_db(sch_db.scheduler_run.task_id==request.post_vars.taskId).select(sch_db.scheduler_run.status,sch_db.scheduler_run.run_output,orderby='id desc').first()
    if not d or not d.run_output:
          return response.json(dict(status="RUNNING", progress="10%" ))
    return response.json(dict(status=d.status, progress=d.run_output))

def createCSV():
    import os
    import datetime
    mode =  request.post_vars.mode
    filename = 'cookies%s-%s.csv' %(mode,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    p = os.path.join(request.folder, 'private', filename)
    task = scheduler.queue_task('createTagFile', pvars=dict(projId=request.post_vars.projId, mode=mode,filename=p), sync_output=2)
    return response.json(dict(filename=filename, taskId=task.id))

@auth.requires_login()
def downFile():
    filename = request.get_vars.filename
    response.headers['Content-type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' %filename
    import os
    path = os.path.join(request.folder, 'private', filename)
    return response.stream(open(path), chunk_size=4096)


def getSyncProgress():
    print 'get sync progress', request.post_vars
    data = lda_db(lda_db.tagSyncLog.id==request.post_vars.logId).select().first()
    allCount = lda_db.executesql('SELECT count(ds_id) FROM Tag_%s' %data.tagProjId)[0][0]
    noCount = lda_db.executesql('SELECT count(ds_id) FROM Tag_%s WHERE ti_id=0' %data.tagProjId)[0][0]
    print allCount-noCount, noCount
    return response.json(dict(data=data, counted=allCount-noCount, noCount=noCount))
   