#coding:utf-8

def hello():
    return "hello world"

def tagRules():
    import datetime
    import gluon.contrib.simplejson as sj
    ts = [sj.loads(r.json) for r in tag_db((tag_db.Tag.company == request.get_vars.media) &
                                                                       (tag_db.Tag.status=="active")).select(tag_db.Tag.json)]
    dt = [int(r.symbol)  for r in tag_db(tag_db.Element.dbCheck=='selected')\
                                          .select(tag_db.Element.symbol)]
    tagRules = dict(MEDIA=request.get_vars.media, 
                                  DATE=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%d'),
                                  DT=dt,
                                  RULES=ts)
    #print request.client
    tag_db.TagPullLog.insert(ip = request.client,
                                                     count = len(ts),
                                                     mode='all',
                                                     startTagId = 0,
                                                     company = request.get_vars.media,
                                                     createDate = datetime.datetime.now()
                                                    )
    return response.json(tagRules)