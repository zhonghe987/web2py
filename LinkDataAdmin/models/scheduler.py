from gluon.scheduler import Scheduler
 
sch_db = DAL('mysql://idexadmin:idex000@180.169.19.150/linkDataAdmin')

DB_NUM = 5000

def __createTagFile(projId, mode, filename):
    import csv
    import time
    where = "SELECT ds_id,cookieId FROM Tag_%s " 
    if mode == 'Incr':
        where = where + "WHERE ti_id=0"
    data = sch_db.executesql(where %projId) 
    f = open(filename,"wb")
    writer = csv.writer(f)
    writer.writerow(['id'.decode('utf8').encode('gbk'),
                                   'cookies'.decode('utf8').encode('gbk'),
                                   'ֵ'.decode('utf8').encode('gbk')])
    c = len(data);
    i = 0
    p = 10
    print '0%'
    for id,cookie in data:
        writer.writerow([id,
                                        cookie.decode('utf8').encode('gbk'),
                                        'None'.decode('utf8').encode('gbk')])
        i += 1        
        d = i/c*100
        if d >= p:
            print '!clear!%d%%' %d
            p += 10

    f.close()
    return 0

def __updateTagDB(filename, tagProjId, logId):
    import time
    import os
    import csv
    fn = os.path.join(request.folder,'uploads',filename)
    f = open(fn, 'r')
    #print 'open file'
    f.readline()
    count = len(f.readlines())
    lda_db(lda_db.tagSyncLog.id==logId).update(status='run', count=count)
    #print count
    f.seek(0)
    f.readline()
    reader = csv.reader(f)    
    value = dict((v,i) for i,v in lda_db.executesql("SELECT ti_id,value FROM TagItem_%s" %tagProjId))
    maxId = lda_db.executesql("SELECT max(ti_id) FROM TagItem_%s" %tagProjId)[0][0]
    if not maxId:
        maxId = 0

    data = []
    i = 0
    p = 10
    count = float(count)
    #print 'start'
    for id, _, v in reader:
        i += 1
        d = (i / count) * 100
        if d > p:
            p += 10
            lda_db(lda_db.tagSyncLog.id==logId).update(up_count=i)
            #time.sleep(10)

        if v == 'None':
            continue

        v = v.decode('GBK')
        ti = value.get(v, None)
        if ti:
            data.append('(%s,%d)' %(id,ti))
        else:
            maxId += 1
            value[v] = maxId
            lda_db.executesql("INSERT INTO TagItem_%s (ti_id,value) VALUES (%d,'%s')" %(tagProjId,maxId,v))
            data.append('(%s,%d)' %(id,maxId))
            
    i = 0
    c = len(data)
    #print c
    while i < c:
        s = ','.join(data[i:i+5000])
        lda_db.executesql("INSERT INTO Tag_%s (ds_id,ti_id) VALUES %s ON DUPLICATE KEY UPDATE ti_id=values(ti_id)" %(tagProjId, s))
        i += 5000

    tagCount = lda_db.executesql("SELECT ti_id,count(ds_id) FROM Tag_%s WHERE ti_id>0 group by ti_id" %tagProjId)
    d = []
    for i, c in tagCount:
        d.append('(%d,%d)' %(i,c))
    lda_db.executesql("INSERT INTO TagItem_%s (ti_id,count) values %s ON DUPLICATE KEY UPDATE count=values(count)" %(tagProjId, ','.join(d)))
    
    lda_db(lda_db.tagSyncLog.id==logId).update(up_count=int(count), status='completed')
    lda_db.commit()
    print 'end'
    return 0

def __updateDataSource():
    import time
    #time.sleep(100)
    orgConf = lda_db(lda_db.orignalDataConf.status=='yes').select().first();
    db = '%s://%s:%s@%s:%d/%s' \
              %(orgConf.dbEngine.lower(), orgConf.dbUser, orgConf.dbPwd,orgConf.host, orgConf.port, orgConf.dbName)

    org_db = DAL(db)

    ds_id = []
    ids = lda_db(lda_db.dataSource.dsStatus == 'run').select(lda_db.dataSource.id, 
                                                                                                                   lda_db.dataSource.cookieDomain)
    for r in ids:
        tbl = 'DS_%d' %r.id
        d = dict(tbl=tbl,id=0, cookdom=r.cookieDomain)
        row = lda_db.executesql('select ds_id  from %s order by ds_id desc limit 0, 1' %tbl)
        if row:
           d['id'] = row[0][0]
        ds_id.append(d)

    min_id = ds_id[0]['id']
    for d in ds_id:
        if min_id > d['id']:
            min_id = d['id']
    
    while 1:
        data = org_db.executesql('select id, cookie_data, cookie_dom from %s where id>%d limit 0, %d' \
                                                            %(orgConf.tableName, min_id, DB_NUM))
        if not data:
            break

        c = len(data)
        for ds in ds_id:
            i = ds['id'] - min_id
            if i >= c:
                continue
            
            d = ["(%d, '%s')" %(id,cook)for id,cook, dom in data[i:] if dom==ds['cookdom']]
            if not d:
                continue

            v = ",".join(d)
            lda_db.executesql("insert into %s (ds_id, cookieId) values %s" %(ds['tbl'],v))
            ds['id'] += c
        min_id += c
    return 0


def __updateDS(table, cookDomain):
    orgConf = lda_db(lda_db.orignalDataConf.status=='yes').select().first();
    if orgConf.dbEngine == 'MySQL':
       db = 'mysql://%s:%s@%s:%d/%s' \
                %(orgConf.dbUser, orgConf.dbPwd,orgConf.host, orgConf.port, orgConf.dbName)

    org_db = DAL(db)

    min_id = 0
    row = lda_db.executesql('select ds_id  from %s order by ds_id desc limit 0, 1' %table)
    if row:
        min_id = row[0][0]

    while 1:
        data = org_db.executesql('select id, cookie_data, cookie_dom from %s where id>%d and cookie_dom="%s" limit 0, %d' \
                                                            %(orgConf.tableName, min_id, cookDomain, DB_NUM))
        if not data:
            break

        d = ["(%d, '%s')" %(id,cook)for id,cook, dom in data]
        v = ",".join(d)
        lda_db.executesql("insert into %s (ds_id, cookieId) values %s" %(table,v))
        min_id = data[-1][0]
    return 0


def __dsToTag(ds, tag):
    ds_id = 0
    while 1:
        data = lda_db.executesql("select ds_id, cookieId from %s where ds_id>%d limit 0, %d" %(ds, ds_id,DB_NUM))
        if not data:
            break

        v = ','.join(["(%d,'%s')" %(id,cookie) for id,cookie in data])
        lda_db.executesql("insert into %s (ds_id,cookieId) values %s"  %(tag,v))
        ds_id =  data[-1][0]
    return 0
 
tasks = dict(createTagFile=__createTagFile,
                       updateTagDB=__updateTagDB,
                       updateDataSource=__updateDataSource,
                       updateDS=__updateDS,
                       dsToTag=__dsToTag
)
 
scheduler = Scheduler(sch_db, tasks)
    

