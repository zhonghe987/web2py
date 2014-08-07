#coding:utf8


LIMIT = 10

@auth.requires_login()
def index():
    import datetime
    dicts={}
    endDate = datetime.datetime.today()+datetime.timedelta(days=1)
    startDate = endDate - datetime.timedelta(days=7)
    count = letv_db.tagLog.id.count()
#    data = letv_db((letv_db.tagLog.date>=startDate) & (letv_db.tagLog.date<=endDate)).select(
#                  letv_db.tagLog.date, letv_db.tagSource.tagName, count,
#                  join=letv_db.tagSource.on(letv_db.tagSource.id==letv_db.tagLog.tagId),
#                  groupby=[letv_db.tagLog.date, letv_db.tagLog.tagId]
#                  )
    data = letv_db.executesql("SELECT  date(date),  tagSource.tagName, count(tl_id) "\
                                                         "FROM tagLog join tagSource on tagSource.t_id=tagId "\
                                                         "group by date(date), tagId order by date(date) desc")
    #print data
    breadcrumb = ['首页']
    tagCount = letv_db(letv_db.tagSource.t_id > 0).count()
    classCount = letv_db(letv_db.midClass.cr_id > 0).count()
    return dict(breadcrumb = breadcrumb,
                          tag_num = tagCount,
                          tag_class = classCount,
                          data = data
                         )

@auth.requires_login()
def tagManage():
    import math
    import datetime
    breadcrumb = ['标签管理']
    bigData = [(name.l_id,name.bigName) for name in letv_db().select(letv_db.bigClass.l_id,letv_db.bigClass.bigName) ]
    bigData.insert(0, (0, '全部'))
    midData = [(name.cr_id,name.midName) for name in letv_db().select(letv_db.midClass.cr_id,letv_db.midClass.midName) ]
    midData.insert(0, (0, '全部'))
    btn = INPUT(_value='搜索',_type='submit',_id='subt')
    form =  SQLFORM.factory(Field('tagname'),
                                                       Field('big',requires = IS_IN_SET(bigData)),
                                                       Field('mid',requires = IS_IN_SET(midData)),
                                                       buttons = [btn]
                                                       )

    tagCondition = (letv_db.tagSource.id>0)
    if form.accepts(request, session):
        if  request.post_vars.big != '0':
            tagCondition =  tagCondition & (letv_db.tagSource.bigClass_id == request.post_vars.big)

        if request.post_vars.mid != '0':
            tagCondition = tagCondition & (letv_db.tagSource.midClass_id == request.vars.mid)

        if  request.post_vars.tagname:
            tagCondition  = tagCondition & (letv_db.tagSource.tagName.like('%%%s%%'%request.post_vars.tagname))
          
    #print 'tagCondition', tagCondition
    tagData = letv_db(tagCondition).select(letv_db.tagSource.id, letv_db.tagSource.tagName,letv_db.tagSource.createDate,
                                                                                   letv_db.bigClass.bigName,letv_db.midClass.midName,
                                                                                   join=[letv_db.bigClass.on(letv_db.bigClass.id==letv_db.tagSource.bigClass_id),
                                                                                              letv_db.midClass.on(letv_db.midClass.id==letv_db.tagSource.midClass_id)],
                                                                                  )
    count = len(tagData)
    pagCount = int(math.ceil(count / LIMIT))
    endDate = datetime.datetime.today()
    startDate = endDate - datetime.timedelta(days=7)
    data = letv_db.executesql("SELECT  A.tagId, count(tl_id) "\
                                                         "FROM (SELECT tl_id, tagId, date FROM tagLog WHERE date(date)>='%s' and date(date)<='%s' ) as A "\
                                                         "join tagSource on tagSource.t_id=tagId "\
                                                         "group by date(date), tagId" %(startDate.date(), endDate.date()))
    tagCount = {}
    for id, cc in data:
        c = tagCount.get(id, 0)
        tagCount[id] = c + cc
    #print 'tagCount', tagCount
    return dict(breadcrumb = breadcrumb,
                          form = form ,
                          tagData = tagData,
                          pagCount = pagCount,
                          count = count,
                          tagCount=tagCount)


def splitPage():
    tagCount = (int(request.vars.count) - 1) * LIMIT
    csdn =()
    if  request.vars.name:
            csdn  = csdn & (letv_db.tagSource.tagName == request.vars.name)
    if  request.vars.big: 
            csdn = csdn & (letv_db.tagSource.l_id == request.vars.big)
    if request.vars.mid:
            csdn = csdn & (letv_db.tagSource.l_id == request.vars.mid)
    data = letv_db(csdn).select(orderby = letv_db.tagSource.t_id,limitby=(tagCount,tagCount + LIMIT))
    import gluon.contrib.simplejson
    return response.json(dict(data = data))


@auth.requires_login()
def  tagEdit():
    import  time
    #print request.vars
    all_data = ['媒资ID','视频名称','企业名称','联系人']
    breadcrumb = ['标签管理','新增标签']
    bigData = [OPTION(items.bigName, _value=items.id) for items in letv_db().select(letv_db.bigClass.bigName,letv_db.bigClass.id)]
    midData = [OPTION(items.midClass.midName,_value=items.midClass.id, _bcId=items.bigClass.id) 
                           for items in letv_db().select(letv_db.midClass.midName,letv_db.midClass.id,letv_db.bigClass.id,
                                                                                  join=letv_db.bigClass.on(letv_db.bigClass.id==letv_db.midClass.b_id))]
    bigData.insert(0,OPTION('请选择',_value='0'))
    midData.insert(0,OPTION('请选择',_value='0'))
    #print 'bigData', bigData
    big = SELECT(bigData,_class="form-control",_id="big",_name="big_class")
    mid = SELECT(midData,_class="form-control",_id="mid",_name="mid_class")
    all = SELECT(all_data,_id="alls",_name="all")
    dictData = {}
    for key in request.vars:
       dictData[key] = request.vars[key]
    data = __genserat(dictData)
    date = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    if data:
       
        if request.vars.tagname:
            letv_db.tagSource.insert(tagName =dictData['tagname'],bigClass_id=dictData['big_class'],midClass_id=dictData['mid_class'],createDate = date)
            tagId = letv_db(letv_db.tagSource.tagName == dictData['tagname']).select(letv_db.tagSource.t_id)
        
        for v in data.values():
            letv_db.ruleGroup.insert(tag_id = tagId[0])
            ruleGroupId = letv_db().select(letv_db.ruleGroup.rg_id,orderby = ~letv_db.ruleGroup.rg_id )
            for k in v:
                letv_db.rules.insert(col_name = k[0],condition_op = k[1],content  = k[2])
                rule_id = letv_db((letv_db.rules.col_name == k[0]) & (letv_db.rules.condition_op == k[1]) &(letv_db.rules.content == k[2])).select(letv_db.rules.r_id)
                letv_db.ruleFilterGroup.insert(rules_id = rule_id[0],ruleGroup_id = ruleGroupId[0])

        redirect(URL('tagManage','tagManage'))
    
    return dict(breadcrumb = breadcrumb, bigClass = big, midClass = mid, all = all)


def __genserat(dicts):
    strs = []
    bao = []
    fill = [] 
    for key in dicts.keys():  
        #print '====',key   
        if 'strsdiv'  in key  and key.find('strsdiv') == 0: 
            strs.append(key)
        if 'baodiv' in key and key.find('baodiv') == 0:   
            bao.append(key)
        if 'filldiv' in  key and key.find('filldiv') == 0 :
            fill.append(key)
    strs = sorted(strs)
    bao = sorted(bao)
    fill = sorted(fill)
    listKeys = zip(strs,bao,fill)
    data = {}
    for i,key in enumerate(listKeys):
            s = dicts[key[0]]
            b = dicts[key[1]]
            f = dicts[key[2]]
            if isinstance(s, list):
                data[i] = zip(s,b,f)
            else:
                data[i] = [(s,b,f)]
    return  data
         


def tagDelete():
    ruleDelete(request.vars.sh_id)
    letv_db(letv_db.tagSource.t_id == request.vars.sh_id ).delete()
    redirect(URL('tagManage','tagManage'))
    
def ruleDelete(id):
    rg_ids = letv_db(letv_db.ruleGroup.tag_id == id ).select(letv_db.ruleGroup.rg_id)
    for g in rg_ids:
        print g
        rule_ids = letv_db(letv_db.ruleFilterGroup.ruleGroup_id == g.id).select(letv_db.ruleFilterGroup.id,letv_db.ruleFilterGroup.rules_id)
        for r in rule_ids:
            letv_db(letv_db.rules.r_id == r.rules_id).delete()
            letv_db(letv_db.ruleFilterGroup.rfg_id == r.id).delete()
        letv_db(letv_db.ruleGroup.rg_id == g.id).delete()
            
def tagLog():
    #tagId = request.get_vars.tagId
    data = letv_db.executesql("SELECT date(date), count(tl_id) "\
                                                         "FROM tagLog WHERE tagId=%s "\
                                                         "group by date(date) order by date(date) desc" %request.get_vars.tagId)
    breadcrumb = ['标签管理','标签历史记录']
    #print len(data), data
    return dict(breadcrumb=breadcrumb,tagName=request.get_vars.tagName, data=data)

def createCSV():
    import os
    import datetime
    mode =  request.post_vars.mode
    filename = 'UserId-Tag-%s-%s.csv' %(mode,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    p = os.path.join(request.folder, 'private', filename)
    task = scheduler.queue_task('createTagFile', pvars=dict(mode=mode,filename=p), sync_output=2)
    return response.json(dict(filename=filename, taskId=task.id))

def getTaskProgress():
    import datetime
    print 'get task progress:', request.post_vars
    d = sch_db(sch_db.scheduler_run.task_id==request.post_vars.taskId).select(sch_db.scheduler_run.status,sch_db.scheduler_run.run_output,orderby='id desc').first()
    if not d or not d.run_output:
          return response.json(dict(status="RUNNING", progress="10%" ))
    return response.json(dict(status=d.status, progress=d.run_output))

@auth.requires_login()
def downFile():
    filename = request.get_vars.filename
    response.headers['Content-type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' %filename
    import os
    path = os.path.join(request.folder, 'private', filename)
    return response.stream(open(path), chunk_size=4096)
	
def showRule():
    dictData = {}
    allRuselt = []
    up = {'containOr':'包含','notContainAnd':'不包含'}
    rgId = letv_db(letv_db.ruleGroup.tag_id == request.vars.sh_id).select(letv_db.ruleGroup.rg_id)
    for group  in rgId:  
        rul = [r.rules_id for r in letv_db(letv_db.ruleFilterGroup.ruleGroup_id  == group.rg_id).select(letv_db.ruleFilterGroup.rules_id)]
        dictData[group.rg_id] = rul
    for k,v in dictData.items():
        data = []
        dic = {}
        for item in v:
            ks = letv_db(letv_db.rules.r_id == item).select(letv_db.rules.condition_op).first()
            if ks.condition_op == "containOr":
                 data.extend([(ks.col_name,up['containOr'],ks.content) for ks in letv_db(letv_db.rules.r_id == item).select(letv_db.rules.col_name,letv_db.rules.content)  ])
            else:
                data.extend([(ks.col_name,up['notContainAnd'],ks.content) for ks in letv_db(letv_db.rules.r_id == item).select(letv_db.rules.col_name,letv_db.rules.content)  ])
        dic[k] = data
        allRuselt.append(dic)
    import gluon.contrib.simplejson
    return response.json(dict(allRuselt = allRuselt))
            