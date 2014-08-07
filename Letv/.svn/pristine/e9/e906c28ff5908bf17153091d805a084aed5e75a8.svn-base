from gluon.scheduler import Scheduler
 
sch_db = DAL('mysql://idexadmin:idex000@180.169.19.150/Letv')


def __containOr(param,data):
    #print 'Contain param:%s, data:%s' %(param, data)
    for p in param:
        if data.find(p) > -1:
            return True
    return False

def __notContainAnd(param, data):
    for p in param:
        if data.find(p) > -1:
            return False
    return True


OP = dict(containOr=__containOr,
                    notContainAnd=__notContainAnd)
 
def __getTagRules(col):
    tagRules = {}
    tags = letv_db().select(letv_db.tagSource.ALL)
    for t in tags:
        group = letv_db(letv_db.ruleGroup.tag_id==t.id).select()
        gl = []
        for g in group:
            rules = letv_db(letv_db.ruleFilterGroup.ruleGroup_id==g.id).select()
            rl = []
            for r in rules:
                re = letv_db(letv_db.rules.id == r.rules_id).select().first()
                rl.append(dict(col=col[re.col_name],param=tuple([s for s in re.content.split(',') if s !='']), op=re.condition_op))
            gl.append(tuple(rl))
        tagRules[t.tagName] = dict(tagId=t.id, ruleGroup=tuple(gl))
    return tagRules

def __tagProcess(tagRules, data):
    t = []
    c = len(data)
    for tag, obj in tagRules.items():
        #print tag 
        for rules in obj['ruleGroup']:            
            for r in rules:
                if r['col'] < c:
                    bRule = OP[r['op']](r['param'],data[r['col']])
                else:
                    bRule = False
                if not bRule: # 规则返回False, 退出本组规则
                    break
            if bRule: # 本组True，退出标签检查
                t.append(dict(tag=tag, tagId=obj['tagId'], userId=data[0]))
                break
    return t


def __tagProcessTask(filename, savefile):
    import csv
    import sys
    import os
    import time
    csv.field_size_limit(10000000)

    b = time.time()
    f = open(filename,'rU')
    col = dict((cn, i) for i, cn in enumerate(f.readline().split(',')))
    tagRules = __getTagRules(col)
    reader = csv.reader(f,quoting=csv.QUOTE_NONE)
    data = []
    for line in reader:
            r = __tagProcess(tagRules, line)
            if r:
                data.extend(r)
    
    e = time.time()
    f.close()
    f = open(savefile,'w')
    f.writelines(['%s-%s-%d\n' %(d['userId'],d['tag'],d['tagId']) for d in data])
    f.close()
    d = ["('%s',%d, now())" %(d['userId'],d['tagId']) for d in data]
    i = 0
    c = len(d)
    #print c
    while i < c:
        s = ','.join(d[i:i+5000])
        letv_db.executesql("INSERT INTO tagLog (userId,tagId, date) VALUES %s" %s)
        letv_db.commit()
        i += 5000
        
    return 'all time: %f, data len: %d, csv line: %d' %((e-b), len(data), reader.line_num)


def __createTagFile(mode, filename):
    import csv
    import time
    tagLog = letv_db(letv_db.tagLog).select(letv_db.tagLog.userId, letv_db.tagLog.date, letv_db.tagSource.tagName,
                                                                                   join=letv_db.tagSource.on(letv_db.tagSource.id==letv_db.tagLog.tagId)
                                                                                  )
    f = open(filename,"wb")
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)
    writer.writerow(['用户ID'.decode('utf8').encode('gbk'),
                                    '标签'.decode('utf8').encode('gbk'),
                                   # '日期'.decode('utf8').encode('gbk')
                                   ])
    c = len(tagLog)*2;
    i = 0
    p = 10
    print '0%'
    
    data = {}
    for r in tagLog:
        tl = data.get(r.tagLog.userId, [])
        tl.append(r.tagSource.tagName)
        data[r.tagLog.userId] = tl
        i += 1        
        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10
  
    for id, tl  in data.items():
        writer.writerow([id.decode('utf8').encode('gbk'), '-'.join(set(tl)).decode('utf8').encode('gbk')])
        #writer.writerow([r.tagLog.userId.decode('utf8').encode('gbk'),
         #                               r.tagSource.tagName.decode('utf8').encode('gbk'),
         #                               r.tagLog.date.strftime('%Y-%m-%d %H:%M:%S').decode('utf8').encode('gbk')])
        i += 1        
        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10
     
    print '!clear!100%'
    f.close()
    return 0
 
tasks = dict(tagProcess = __tagProcessTask,
                       createTagFile = __createTagFile
)
 
scheduler = Scheduler(sch_db, tasks)
    

