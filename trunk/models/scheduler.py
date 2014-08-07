#coding:utf-8

from gluon.scheduler import Scheduler
 
sch_db = DAL('mysql://idexadmin:idex000@180.169.19.150/tagRuleAdmin',migrate_enabled=False)

SQL_NUM = 5000

def __createContentFile(filename):
    import csv
    
    fields = [d.decode('utf8').encode('gbk') for d in tag_db.ContentInfo.fields]
    fields.remove('createDate')
    fields.remove('c_id')

    f = open(filename,"wb")
    writer = csv.writer(f)
    writer.writerow(fields)
    c = tag_db(tag_db.ContentInfo).count()
    rows = tag_db(tag_db.ContentInfo).select()
    i = 0
    p = 20
    print '20%'
    for r in rows:
        d = []
        for fd in fields:
            d.append(r[fd].decode('utf8').encode('gbk'))
        writer.writerow(d)
        i += 1        
        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10
    f.close()
    print '!clear!100%'
    return 0

def __updateContentInfo(filename, mode):
    import csv
    import os
    import datetime
    
    fn = os.path.join(request.folder,'uploads',filename)
    f = open(fn, 'r')
    fileSize = 1024*1024
    c = 0
    while 1:
        b = f.read(fileSize)
        if not b:
            break
        c += b.count('\n')
    f.seek(0)
    t1 = [ d.strip() for d in f.readline().split(',')]
    t2 = set(tag_db.ContentInfo.fields)
    t = set(t1)& t2
    if not t:
        print '!clear!100%'
        return -101

    inx = []
    for tt in t:
        inx.append(t1.index(tt));
    t = list(t)
    t.append('createDate')
    fields = ','.join(t)
    e = 'GBK'
    #print c
    try:
        f.readline().decode(e)
    except:
        e = 'UTF-8'
    #print e
    f.seek(0)
    f.readline()
    reader = csv.reader(f) 
    if mode == 'all':
        tag_db.ContentInfo.truncate()
    i = 0
    v = []
    p = 25
    for d in reader:
        if len(','.join([ dd for dd in d if dd]).split(','))>2:
            vv = []
            for ix in inx:
                vv.append("'%s'" %d[ix].decode(e))
            vv.append("'%s'" %datetime.datetime.now())
            v.append("(%s)" %','.join(vv))
        i += 1
        if i == SQL_NUM:
            tag_db.executesql("INSERT INTO ContentInfo (%s) VALUES %s ON DUPLICATE KEY UPDATE createDate=values(createDate)" %(fields,','.join(v)))
            v = []
            i = 0

        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10

    if v:
        tag_db.executesql("INSERT INTO ContentInfo (%s) VALUES %s ON DUPLICATE KEY UPDATE createDate=values(createDate)" %(fields,','.join(v)))
    tag_db.commit()
    print '!clear!100%'
    return 0

def __contentCheck(check, data):
    import math
    #data = data.replace('|', '|')
    data = set([d.strip() for d in data.split('|') if d != ''])
#    l = []
#    for d in d1:
#        l.extend([dd.strip() for dd in d.split('，') if dd !=''])
#    data = set(dl)
    print '20%'
    f = '%s' %check
    c = tag_db(tag_db.ContentInfo.id).count()
    n = int(math.ceil(c/5000.0))
    l = 80.0/n
    i = 0
    p = 20
    for m in xrange(n):
        r = tag_db(tag_db.ContentInfo.id > i).select(tag_db.ContentInfo.id,
                                                                                              tag_db.ContentInfo[f],
                                                                                              limitby=(0,5000))
        s = data - set([d[f] for d in r])
        if not s:
            break
        i = r[-1].id
        p += l
        data = s 
        print '!clear!%d%%' %p

    print '!clear!100%'
    return ','.join(s)

def __createTagRuleFile(filename, company):
    import datetime
    import gluon.contrib.simplejson as sj
    f = open(filename,"wb")
    condition = (tag_db.Tag.company==company) & (tag_db.Tag.status=='active')
    c = tag_db(condition).count()
    
    i = 0
    p = 15
    l = []
    print '15%'
    while i < c:
        rows = tag_db(condition).select(tag_db.Tag.json,
                                                                       limitby=(i, SQL_NUM)
                                                                      )
        l.extend([sj.loads(r.json) for r in rows])
        i += SQL_NUM
        if i > c:
            i = c        
        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10
     
    dt = [int(r.symbol)  for r in tag_db(tag_db.Element.dbCheck=='selected')\
                                          .select(tag_db.Element.symbol)]
    t = dict(MEDIA=company,
                   DATE = datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S'),
                   DT = dt,
                   RULES = l
                  )
    f.write(sj.dumps(t))
    print '!clear!100%'
    f.close()
    return 0
 
tasks = dict(createContentFile=__createContentFile,
                       updateContentInfo=__updateContentInfo,
                       #contentCheck = __contentCheck,
                       createTagRuleFile = __createTagRuleFile
)
 
scheduler = Scheduler(sch_db, tasks)
    

