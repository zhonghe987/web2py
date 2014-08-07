#coding:utf8

import datetime
import math

LIST_NUM = 10
FMT_DATETIME = "%Y%m%d%H%M%S"

breadcrumb = ['标签管理']

#@auth.requires((auth.user.classes == 'admin' or auth.user.classes == 'user'  or auth.user.classes == 'visit') and auth.user.status == '1', requires_login = True)
@auth.requires(auth.user and auth.user.status == '1' , requires_login = True)
def index():
    import gluon.contrib.simplejson as sj
    cnd = dict(tagName='', status='all')
    status = [('all', '全部'), ('active','激活'),('not active', '未激活')]
    btn = INPUT(_value='搜索',_type='submit',_id='sub')
    form =  SQLFORM.factory(Field('tagName'),
                                                      Field('status', requires = IS_IN_SET(status)),
                                                      buttons = [btn]
                                                      )
    condition = (tag_db.Tag.company==auth.user.company)
    if form.accepts(request,session):
        if request.post_vars.status != 'all':
            condition = condition & (tag_db.Tag.status == request.post_vars.status)
            cnd['status'] = request.post_vars.status
        
        if request.post_vars.tagName:
            condition = condition & (tag_db.Tag.name.like("%%%s%%" %request.post_vars.tagName))
            cnd['tagName'] = request.post_vars.tagName

    data = tag_db(condition).select(tag_db.Tag.id,
                                                                     tag_db.Tag.name,
                                                                     tag_db.Tag.json,
                                                                     tag_db.Tag.status,
                                                                     tag_db.Tag.tagDesc,
                                                                     tag_db.Tag.createDate,
                                                                     limitby=(0,LIST_NUM),
                                                                     orderby="createDate desc",
                                                                    )
    dc = tag_db(condition).count()
    pageCount = int(math.ceil(dc / float(LIST_NUM))) 
    dimData = dict((r.symbol,  r.name) for r in tag_db((tag_db.Dimension.status=='enable'))\
                                                                                                   .select(tag_db.Dimension.name, 
                                                                                                                 tag_db.Dimension.symbol))
    d = tag_db((tag_db.Element.status=='enable'))\
                          .select(tag_db.Element.id,
                                        tag_db.Element.name, 
                                        tag_db.Element.symbol,
                                        tag_db.Element.dbCheck,
                                        tag_db.Dimension.name,
                                        join=tag_db.Element.on(tag_db.Element.d_id==tag_db.Dimension.id))
    eleDate = [r for r in d if r.Dimension.name=='时间维度']
    eleContent = dict((r.Element.dbCheck, r.Element.name ) for r in d if r.Dimension.name=='内容维度')
    #print dimData
    return dict(breadcrumb = breadcrumb,
                          form = form,
                          data = data,
                          count = dc,
                          pageCount = pageCount,
                          find = cnd,
                          dim = sj.dumps(dimData),
                          eleContent = sj.dumps(eleContent),
                          eleDate = eleDate
                         )

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def new():
    dimData = tag_db((tag_db.Dimension.status=='enable')).select(tag_db.Dimension.name, 
                                                                                                                                  tag_db.Dimension.symbol)
    eleData = tag_db((tag_db.Element.status=='enable')).select(tag_db.Element.name, 
                                                                                                                           tag_db.Element.symbol,
                                                                                                                           tag_db.Element.dbCheck, 
                                                                                                                           tag_db.Dimension.name,
                                                                                                                           join=tag_db.Element.on(tag_db.Element.d_id==tag_db.Dimension.id)
                                                                                                                          )
    
    if request.post_vars.name:
        tag_db.Tag.insert(name=request.post_vars.name,
                                           tagDesc = request.post_vars.desc,
                                           status = request.post_vars.status,
                                           json = request.post_vars.rules.replace('，',','),
                                           company = auth.user.company,
                                           createDate = datetime.datetime.now()
                                          )
    breadcrumb.append('新增标签')
    return dict(breadcrumb = breadcrumb,
                           dimData = dimData,
                           eleData = eleData,
                         )

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def tagPaginate():
    #print request.post_vars
    condition = (tag_db.Tag.id>0)     
    if request.post_vars.tagName:
        condition = condition & (tag_db.Tag.name.like("%%%s%%" %request.post_vars.tagName))


    startId = (int(request.post_vars.page)-1) * LIST_NUM
    data = tag_db(condition).select( tag_db.Tag.id,
                                                                     tag_db.Tag.name,
                                                                     tag_db.Tag.json,
                                                                     tag_db.Tag.status,
                                                                     tag_db.Tag.tagDesc,
                                                                     tag_db.Tag.createDate,
                                                                     limitby=(startId,startId+LIST_NUM),
                                                                     orderby="createDate desc",
                                                                   ).as_list()
    #print data
    return response.json(dict(data=data, startId=startId+1))


#def contentCheck():
#    #print request.post_vars
#    task = scheduler.queue_task('contentCheck', 
#                                                             pvars=dict(check = request.post_vars.check,
#                                                                                   data = request.post_vars.data), 
#                                                             sync_output=2)
#    #print task
#    return '%d' %task.id
    

#def getCheckInfo():
    #print 'get check info:', request.post_vars
#    d = sch_db(sch_db.scheduler_run.task_id==request.post_vars.taskId) \
#                         .select(sch_db.scheduler_run.status,
#                                        sch_db.scheduler_run.run_output,
#                                        sch_db.scheduler_run.run_result,
#                                        orderby='id desc').first()
#    if not d or not d.run_output:
#          return response.json(dict(status="RUNNING", progress="10%", data='' ))
#    return response.json(dict(status=d.status, progress=d.run_output, data=d.run_result))

def checkElement():
    import math
    #data = request.post_vars.data.replace('|', '|')
    data = set([d.strip() for d in request.post_vars.data.split('|') if d != ''])
    f = '%s' %request.post_vars.check
    c = tag_db(tag_db.ContentInfo.id).count()
    n = int(math.ceil(c/5000.0))
    i = 0
    for m in xrange(n):
        r = tag_db(tag_db.ContentInfo.id > i).select(tag_db.ContentInfo.id,
                                                    tag_db.ContentInfo[f],
                                                    limitby=(0,5000))
        s = data - set([d[f] for d in r])
        if not s:
            break
        i = r[-1].id
        data = s 
    return ','.join(s)


def statusUpdate():
    import gluon.contrib.simplejson as sj
    #print request.post_vars
    data =  sj.loads(request.post_vars.data)
    for id, status in data:
        tag_db(tag_db.Tag.id==id).update(status=status)
    return 'ok'

def tagDel():
    #print request.post_vars

    tag_db(tag_db.Tag.id == request.post_vars.id).delete()
    condition = (tag_db.Tag.company==auth.user.company)
    condition = condition & (tag_db.Tag.id != request.post_vars.id)
    if request.post_vars.status != 'all':
        condition = condition & (tag_db.Tag.status == request.post_vars.status)
    #print condition
    d = ''
    startId = 0
    page = 0
    pc = 0
    dc = tag_db(condition).count()
    #print 'dc->',dc
    if dc: # 有记录
        pc = int(math.ceil(dc / float(LIST_NUM))) 
        startId = int(request.post_vars.num)
        page = int(math.ceil((startId+1)/float(LIST_NUM)))
        #print pc, page, startId
        if pc < int(request.post_vars.pageCount) and pc < page: # 减少一页
                #print u'减少一页'
                page = pc
                startId = (pc-1)*LIST_NUM
                d = tag_db(condition).select(tag_db.Tag.id,
                                                                         tag_db.Tag.name,
                                                                         tag_db.Tag.json,
                                                                         tag_db.Tag.status,
                                                                         tag_db.Tag.tagDesc,
                                                                         tag_db.Tag.createDate,
                                                                         limitby=(startId,startId+LIST_NUM),
                                                                         orderby="createDate desc",
                                                                        ).as_list()
        else: # 当前页
            #print u'当前页'
            startId = page*LIST_NUM-1
            #print startId, page, pc
            d = tag_db(condition).select(tag_db.Tag.id,
                                                                          tag_db.Tag.name,
                                                                          tag_db.Tag.json,
                                                                          tag_db.Tag.status,
                                                                          tag_db.Tag.tagDesc,
                                                                          tag_db.Tag.createDate,
                                                                          limitby=(startId,startId+1),
                                                                          orderby="createDate desc",
                                                                         ).as_list()
            if not d:
                d = ''
    #print d
    return response.json(dict(data=d,
                                                     count = dc,
                                                     num = startId+1,
                                                     pageCount=pc, 
                                                     page=page))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def edit():
    #print request.vars.id
    data = tag_db(tag_db.Tag.id == request.vars.id)\
                                .select(tag_db.Tag.id,
                                              tag_db.Tag.name,
                                              tag_db.Tag.tagDesc,
                                              tag_db.Tag.status,
                                              tag_db.Tag.json)\
                                .first()
    dimData = tag_db((tag_db.Dimension.status=='enable')).select(tag_db.Dimension.name, 
                                                                                                                                  tag_db.Dimension.symbol)
    eleData = tag_db((tag_db.Element.status=='enable'))\
                                        .select(tag_db.Element.name, 
                                                      tag_db.Element.symbol,
                                                      tag_db.Element.dbCheck, 
                                                      tag_db.Dimension.name,
                                                      join=tag_db.Element.on(tag_db.Element.d_id==tag_db.Dimension.id)
                                                     )
    if request.post_vars.name:
        #print request.post_vars
        tag_db(tag_db.Tag.id==request.vars.id)\
                              .update(name=request.post_vars.name,
                                                tagDesc = request.post_vars.desc,
                                                status = request.post_vars.status,
                                                json = request.post_vars.rules,
                                              ) 
        return 'ok'
    breadcrumb.append("编辑标签")
    #print data
    return dict(breadcrumb = breadcrumb,
                          data = data,
                          dimData = dimData,
                          eleData = eleData
                         )

def tagDown():
    import os
    #print 'tag down', datetime.datetime.now().strftime(FMT_DATETIME)
    filename = 'tagRuels-%s.json' %datetime.datetime.now().strftime(FMT_DATETIME)
    p = os.path.join(request.folder, 'private', filename)
    #print p
    task = scheduler.queue_task('createTagRuleFile', 
                                                            pvars=dict(filename=p, company=auth.user.company), 
                                                            sync_output=2)
    #print task
    return response.json(dict(taskId=task.id, 
                                                      filename=filename))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def downFile():
    import os
    filename = request.get_vars.filename
    response.headers['Content-type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' %filename
    path = os.path.join(request.folder, 'private', filename)
    return response.stream(open(path), chunk_size=4096)

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def getTaskProgress():
    #print 'get task progress:', request.post_vars
    d = sch_db(sch_db.scheduler_run.task_id==request.post_vars.taskId) \
                         .select(sch_db.scheduler_run.status,
                                        sch_db.scheduler_run.run_output,
                                        orderby='id desc').first()
    if not d or not d.run_output:
          return response.json(dict(status="RUNNING", progress="10%" ))
    return response.json(dict(status=d.status, progress=d.run_output))

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def eleDateSave():
    import gluon.contrib.simplejson as sj
    #print request.post_vars
    data =  sj.loads(request.post_vars.data)
    for id, status in data:
        tag_db(tag_db.Element.id==id).update(dbCheck=status)
    return 'ok'

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def checkTagName():
    #print request.post_vars
    cnd = (tag_db.Tag.name==request.post_vars.name)
    if request.post_vars.id:
        cnd = cnd & (tag_db.Tag.id != request.post_vars.id)
    r = tag_db(cnd).select(tag_db.Tag.id).first()
    #print r
    if r:
        return '102'
    else:
        return '0'