#coding:utf8

import datetime
import math

LIST_NUM = 20

FMT_DATE = '%Y-%m-%d'
DT = datetime.timedelta(hours=23,minutes=59,seconds=59)

#@auth.requires((auth.user.classes == 'admin' or auth.user.classes == 'user'  or auth.user.classes == 'visit') and auth.user.status == '1', requires_login = True)
@auth.requires(auth.user and auth.user.status == '1' , requires_login = True)
def index():
    #print 'rq->', request.post_vars
    today = datetime.datetime.today().replace(hour=0,minute=0,second=0)
    cnd = dict(company='全部', 
                          startDate=today, 
                          endDate=today+DT)
    btn = INPUT(_value='搜索',_type='submit',_id='sub')
    form =  SQLFORM.factory( Field('startDate'),
                                                       Field('endDate'),
                                                       buttons = [btn]
                                                      )
    condition = (tag_db.TagPullLog.id>0) & (tag_db.TagPullLog.company == auth.user.company)
    if form.accepts(request, session):
        if request.post_vars.startDate:
            cnd['startDate'] = datetime.datetime.strptime(request.post_vars.startDate, FMT_DATE)

        if request.post_vars.endDate:
            d = datetime.datetime.strptime(request.post_vars.endDate, FMT_DATE)
            cnd['endDate'] = d + DT

    condition = condition & (tag_db.TagPullLog.createDate>=cnd['startDate']) \
                                               & (tag_db.TagPullLog.createDate<=cnd['endDate'])
    #print condition
    data = tag_db(condition).select(tag_db.TagPullLog.company,
                                                                     tag_db.TagPullLog.ip,
                                                                     tag_db.TagPullLog.count,
                                                                     #tag_db.TagPullLog.mode,
                                                                     tag_db.TagPullLog.createDate,
                                                                     orderby = 'createDate desc',
                                                                     limitby=(0,LIST_NUM)
                                                                    )
    dc = tag_db(condition).count()
    pageCount = int(math.ceil(dc / float(LIST_NUM)))
    breadcrumb = ['日志']
    return dict(breadcrumb = breadcrumb,
                          form = form,
                          data = data,
                          startDate = cnd['startDate'].strftime(FMT_DATE),
                          endDate = cnd['endDate'].strftime(FMT_DATE),
                          count = dc,
                          pageCount = pageCount
                         )

@auth.requires(auth.user and (auth.user.classes == 'admin' or auth.user.classes == 'user') and auth.user.status == '1' , requires_login = True)
def logPaginate():
    #print request.post_vars
    condition = (tag_db.TagPullLog.id>0)  & (tag_db.TagPullLog.company == auth.user.company)     
    startDate = datetime.datetime.strptime(request.post_vars.startDate, FMT_DATE)
    endDate = datetime.datetime.strptime(request.post_vars.endDate, FMT_DATE) + DT
    condition = condition & (tag_db.TagPullLog.createDate>=startDate) \
                                               & (tag_db.TagPullLog.createDate<=endDate)
    startId = (int(request.post_vars.page)-1) * LIST_NUM
    data = tag_db(condition).select( tag_db.TagPullLog.ip,
                                                                     tag_db.TagPullLog.count,
                                                                     tag_db.TagPullLog.mode,
                                                                     tag_db.TagPullLog.createDate,
                                                                     orderby='createDate desc',
                                                                     limitby=(startId,startId+LIST_NUM),
                                                                    ).as_list()
    #print data
    return response.json(dict(data=data, startId=startId+1))