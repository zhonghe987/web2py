#coding:utf8
def user():
    if  "not_authorized":
        return dict()
    
def errorPage():
    return dict()

    
def index():
    tagCount = tag_db(tag_db.Tag.t_id > 0).count()
    contCount = tag_db(tag_db.ContentInfo.c_id > 0).count()
    data = tag_db(tag_db.TagPullLog.tp_id > 0).select(tag_db.TagPullLog.ip,tag_db.TagPullLog.count,tag_db.TagPullLog.createDate,orderby = ~tag_db.TagPullLog.tp_id,limitby=(0,3))
    logCount = tag_db(tag_db.TagPullLog.tp_id > 0).count()
    dateF = tag_db(tag_db.TagPullLog.tp_id > 0).select(tag_db.TagPullLog.createDate).first()
    dateL = tag_db(tag_db.TagPullLog.tp_id > 0).select(tag_db.TagPullLog.createDate).last()
    
    return dict(breadcrumb=['首页'],tagCount = tagCount,contCount = contCount,data = data,logCount = logCount,first = dateF,last = dateL )