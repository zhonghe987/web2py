#coding:utf8

import datetime
import math

LIST_NUM = 10

breadcrumb = ['符号管理']

#@auth.requires(auth.user.classes == 'admin' or auth.user.classes == 'user' or auth.user.classes == 'visit' or auth.user.status == '1', requires_login = True)
@auth.requires( auth.user and auth.user.classes == 'admin' and  auth.user.status == '1', requires_login = True)  
def index():
    dimData = tag_db(tag_db.Dimension.status=='enable').select(tag_db.Dimension.d_id,tag_db.Dimension.symbol,
                                                                                                                              tag_db.Dimension.name,
                                                                                                                              tag_db.Dimension.dimDesc,
                                                                                                                              )
    eleData = tag_db(tag_db.Element.status=='enable')\
                                       .select(tag_db.Element.e_id,
                                               tag_db.Element.symbol,
                                                      tag_db.Element.name,
                                                      tag_db.Element.eleDesc,
                                                      tag_db.Dimension.name,
                                                      join=tag_db.Element.on(tag_db.Element.d_id==tag_db.Dimension.id)
                                                     )
    
    return dict(breadcrumb = breadcrumb,
                           dimData = dimData,
                           eleData = eleData
                         )

@auth.requires(auth.user and auth.user.classes == 'admin'  and auth.user.status == '1' , requires_login = True)
def dimNew():
    status = [('not support','不支持'),('enable','支持')]
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    form = SQLFORM.factory(Field('symbol',requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(tag_db,'Dimension.symbol')]),
                                                      Field('name',requires = IS_NOT_EMPTY()),
                                                      Field('desc','text'),
                                                      Field('status', requires=IS_IN_SET(status)),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    if form.accepts(request,session):          
        tag_db.Dimension.insert(symbol = request.post_vars.symbol,
                                                        name = request.post_vars.name,
                                                        dimDesc = request.post_vars.desc,
                                                        status = request.post_vars.status,
                                                        createDate = datetime.datetime.now())

        redirect(URL('index'))
    breadcrumb.append('新增维度')
    return dict(form  = form,breadcrumb  = breadcrumb )


@auth.requires(auth.user and auth.user.classes == 'admin' and auth.user.status == '1' , requires_login = True)
def eleNew():
    status = [('not support','不支持'),('enable','支持')]
    check = [(f,f) for f in tag_db.ContentInfo.fields if f != 'c_id' and f!='createDate']
    check.insert(0,('', '无'))
    dimens = [(k.d_id,k.name) for k in tag_db(tag_db.Dimension.status =='enable').select(tag_db.Dimension.name,tag_db.Dimension.d_id,orderby=tag_db.Dimension.d_id)]
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    form = SQLFORM.factory(Field('symbol',requires = IS_NOT_EMPTY()),
                                                      Field('name',requires = IS_NOT_EMPTY()),
                                                      Field('desc','text'),
                                                      Field('status', requires=IS_IN_SET(status)),
                                                      Field('check', requires=IS_IN_SET(check)),
                                                      Field('dimens', requires=IS_IN_SET(dimens)),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    if form.accepts(request,session):
       # print request.vars
        tag_db.Element.insert(symbol = request.post_vars.symbol,
                                                    name = request.post_vars.name,
                                                    eleDesc = request.post_vars.desc,
                                                    status = request.post_vars.status,
                                                    dbCheck = request.post_vars.check,
                                                    d_id = request.vars.dimens,
                                                    createDate = datetime.datetime.now())

        redirect(URL('index'))
    breadcrumb.append('新增元素')
    return dict(breadcrumb  = breadcrumb,
                          form=form,
                         )


@auth.requires(auth.user and auth.user.classes == 'admin' and auth.user.status == '1' , requires_login = True)
def itemEdit():
    breadcrumb.append('元素修改')
    status = [('not support','不支持'),('enable','支持')]
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    classes = [(k.d_id,k.name)for k in tag_db(tag_db.Dimension.status == 'enable').select(tag_db.Dimension.name,tag_db.Dimension.d_id)]
    
    data = tag_db(tag_db.Element.e_id == request.vars.ids).select(
                                               tag_db.Element.symbol,
                                                      tag_db.Element.name,
                                                      tag_db.Element.eleDesc,
                                                      tag_db.Element.status,
                                                      tag_db.Dimension.d_id,
                                                      join=tag_db.Element.on(tag_db.Element.d_id==tag_db.Dimension.id)
                                                     ).first()
    
    
    form = SQLFORM.factory(Field('symbol',requires = IS_NOT_EMPTY()),
                                                      Field('name',requires = IS_NOT_EMPTY()),
                                                      Field('status',requires = IS_IN_SET(status)),
                                                      Field('eleDesc','text'),
                                                      Field('classes',requires=IS_IN_SET(classes)),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    
    if form.accepts(request,session):
        tag_db(tag_db.Element.e_id == request.vars.ids).update(symbol = request.vars.symbol,
                                                               name=request.vars.name,
                                                               status = request.vars.status,
                                                               d_id = request.vars.classes,
                                                               eleDesc = request.vars.eleDesc)
        redirect(URL('symbolManage','index'))
        
        
    return dict(breadcrumb = breadcrumb,form = form,data = data)

@auth.requires(auth.user and auth.user.classes == 'admin' and auth.user.status == '1' , requires_login = True)
def itemDelet():
    tag_db(tag_db.Element.e_id == request.post_vars.ids).delete()
    return 0


def dimeEdit():
    breadcrumb.append('维度修改')
    status = [('not support','不支持'),('enable','支持')]
    btn_sub = INPUT(_value='保存',_type='submit',_id='sub')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    data = tag_db(tag_db.Dimension.d_id == request.vars.id).select(tag_db.Dimension.name,
                                                            tag_db.Dimension.symbol,
                                                            tag_db.Dimension.dimDesc,
                                                            tag_db.Dimension.status
                                                            ).first()
    print '--',data
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()),
                           Field('symbol',requires = IS_NOT_EMPTY()),
                           Field('dimDesc','text'),
                           Field('status',requires=IS_IN_SET(status)),
                           buttons = [btn_sub, btn_cnl]
                           )
    
    if form.accepts(request,session):
        print request.vars
        tag_db(tag_db.Dimension.d_id == request.vars.id).update(name = request.vars.name,
                                                                symbol = request.vars.symbol,
                                                                status = request.vars.status,
                                                                dimDesc = request.vars.dimDesc,
                                                                
                                                                )
        redirect(URL('symbolManage','index'))
        
    return dict(breadcrumb = breadcrumb,form = form ,data = data)
         
def dimDlete():
      tag_db(tag_db.Dimension.d_id == request.vars.id).delete()
      return 0  
