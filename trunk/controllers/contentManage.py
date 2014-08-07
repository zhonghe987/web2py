#coding:utf8

import datetime
import math
import os

LIST_NUM = 20

FMT_DATETIME = "%Y%m%d%H%M%S"

breadcrumb = ['内容库管理']

#@auth.requires((auth.user.classes == 'admin' or auth.user.classes == 'user'  or auth.user.classes == 'visit') and auth.user.status == '1', requires_login = True)
@auth.requires(auth.user and auth.user.status == '1' , requires_login = True)
def index():
    cnd = dict(channel="全部", area="全部")
    chlData = [r.channel for r in tag_db().select(tag_db.ContentInfo.channel,
                                                                                            groupby=tag_db.ContentInfo.channel)
                        ]
    chlData.insert(0,"全部")
    areaData = [r.area for r in tag_db().select(tag_db.ContentInfo.area,
                                                                                       groupby=tag_db.ContentInfo.area)
                           ]
    areaData.insert(0,"全部")
    btn_sub  = INPUT(_value='搜索',_type='submit',_id='sub')
    form = SQLFORM.factory(Field('channel',requires = IS_IN_SET(chlData)),
                                                      Field('area',requires = IS_IN_SET(areaData)),
                                                      buttons = [btn_sub]
                                                     )
    condition = (tag_db.ContentInfo.id>0)
    if form.accepts(request,session):     
        if request.post_vars.channel != "全部":
            condition = condition & (tag_db.ContentInfo.channel == request.post_vars.channel)
            cnd['channel']= request.post_vars.channel

        if request.post_vars.area != "全部":
            condition = condition & (tag_db.ContentInfo.area == request.post_vars.area)
            cnd['area']= request.post_vars.area

    data = tag_db(condition).select( tag_db.ContentInfo.c_id,
                                                                     tag_db.ContentInfo.channel,
                                                                     tag_db.ContentInfo.album,
                                                                     tag_db.ContentInfo.area,
                                                                     limitby=(0,LIST_NUM)
                                                                   )
    dc =tag_db(condition).count()
    pc = int(math.ceil(dc/float(LIST_NUM)))
    return dict(breadcrumb = breadcrumb,
                          form = form,
                          find = cnd,
                          data = data,
                          count = dc,
                          pageCount = pc
                         )

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def new():
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    form = SQLFORM.factory(Field('channel',requires = IS_NOT_EMPTY()),
                                                      Field('area',requires = IS_NOT_EMPTY()),
                                                      Field('album',requires = IS_NOT_EMPTY()),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    if form.accepts(request,session):          
        tag_db.ContentInfo.insert(channel = request.post_vars.channel,
                                                            area = request.post_vars.area,
                                                            album = request.post_vars.album,
                                                            site = auth.user.company,
                                                            createDate = datetime.datetime.now())

        redirect(URL('index'))
    breadcrumb.append('新增内容')
    return dict(form  = form,breadcrumb  = breadcrumb )

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def contentPaginate():
    #print request.post_vars
    condition = (tag_db.ContentInfo.id>0)     
    if request.post_vars.channel != "全部":
        condition = condition & (tag_db.ContentInfo.channel == request.post_vars.channel)

    if request.post_vars.area != "全部":
        condition = condition & (tag_db.ContentInfo.area == request.post_vars.area)

    startId = (int(request.post_vars.page)-1) * LIST_NUM
    data = tag_db(condition).select( tag_db.ContentInfo.c_id,
                                                                     tag_db.ContentInfo.channel,
                                                                     tag_db.ContentInfo.album,
                                                                     tag_db.ContentInfo.area,
                                                                     limitby=(startId,startId+LIST_NUM)
                                                                   ).as_list()
    #print data
    return response.json(dict(data=data, startId=startId+1))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def downContent():
    #print request.post_vars
    filename = 'content-%s.csv' %datetime.datetime.now().strftime(FMT_DATETIME)
    p = os.path.join(request.folder, 'private', filename)
    task = scheduler.queue_task('createContentFile', pvars=dict(filename=p), sync_output=2)
    return response.json(dict(taskId=task.id, filename=filename))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def downFile():
    filename = request.get_vars.filename
    response.headers['Content-type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' %filename
    path = os.path.join(request.folder, 'private', filename)
    return response.stream(open(path), chunk_size=4096)

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def getTaskProgress():
    #print 'content -> get task progress:', request.post_vars
    d = sch_db(sch_db.scheduler_run.task_id==request.post_vars.taskId) \
                         .select( sch_db.scheduler_run.status,
                                        sch_db.scheduler_run.run_output,
                                        sch_db.scheduler_run.run_result,
                                        orderby='id desc').first()
    #print d
    if not d or not d.run_output:
          return response.json(dict(status="RUNNING", progress="10%", result='' ))
    return response.json(dict(status=d.status, progress=d.run_output, result=d.run_result))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True) 
def uploadFiles():
    #print 'upload file', request.post_vars.mode
    p = os.path.join(request.folder,'uploads')
    fn = os.path.join(p,'%s' %request.vars.name)
    #print fn
    with open(fn,'wb') as f:
        f.write(request.vars.file.value)
    d =  datetime.datetime.now()   
    new = os.path.join(p, 'content-%s.csv' %d.strftime('%Y%m%d%H%M%S'))
    os.rename(fn, new)
    #print 'fin'
    task = scheduler.queue_task('updateContentInfo', pvars=dict(filename=new, mode=request.post_vars.mode), sync_output=2, timeout=86400)
    #print task
    return  '%d' %task.id


@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True) 
def conEdit():
    breadcrumb.append('内容修改')
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    data = tag_db(tag_db.ContentInfo.c_id == request.vars.ids)\
                                .select(tag_db.ContentInfo.channel,
                                              tag_db.ContentInfo.album,
                                              tag_db.ContentInfo.area,
                                             ).first()
    form = SQLFORM.factory(Field('channel',requires = IS_NOT_EMPTY()),
                                                      Field('area',requires = IS_NOT_EMPTY()),
                                                      Field('album',requires = IS_NOT_EMPTY()),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    if form.accepts(request,session):
        tag_db(tag_db.ContentInfo.c_id == request.vars.ids)\
                        .update(channel = request.vars.channel,
                                         album = request.vars.album,
                                         area = request.vars.area,
                                        )
        redirect(URL('contentManage','index'))
    return dict(data = data,form = form,breadcrumb = breadcrumb)


@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True) 
def conDelete():
    #print 'del', request.post_vars
    tag_db(tag_db.ContentInfo.id == request.post_vars.ids).delete()
    return 'ok'