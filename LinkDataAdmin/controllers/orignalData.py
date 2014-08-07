# -*- coding: utf-8 -*-

def orignalDataConf():
    btn = INPUT(_value='保存',_type='submit',_id='subt')
    dbEngine = [('MySQL','MySQL'),('MSSQL','MSSQL')]
    status = [('no','不选中'),('yes','选中')]
    #engine = SELECT(dbEngine,_class="form-control form-input",_id="db_engine",_name="db_engine")
    form =  SQLFORM.factory(Field('confName',requires = IS_NOT_EMPTY()),
                            Field('dbEngine',requires = IS_IN_SET(dbEngine)),
                            Field('host',requires = IS_NOT_EMPTY()),
                            Field('port',requires = IS_NOT_EMPTY()),
                            Field('dbName',requires = IS_NOT_EMPTY()),
                            Field('tableName',requires = IS_NOT_EMPTY()),
                            Field('status',requires=IS_IN_SET(status)),
                            Field('dbUser',requires = IS_NOT_EMPTY()),
                            Field('dbPwd',requires = IS_NOT_EMPTY()),
                            buttons = [btn],
                            )
    if form.accepts(request,session):
        lda_db.orignalDataConf.insert(name=form.vars.confName,
                                      dbEngine = form.vars.dbEngine,
                                      host= form.vars.host,
                                      port = form.vars.port,
                                      dbName = form.vars.dbName,
                                      tableName = form.vars.tableName,
                                      dbUser = form.vars.dbUser,
                                      dbPwd = form.vars.dbPwd,
                                      status = form.vars.status)
        redirect(URL('orignalData','orignalIndex'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form-> %s' %auth.user
    return dict(breadcrumb=['数据源配置管理','数据源配置'], panelTitle='新增源数据配置',form = form)


def orignalIndex():
    data = lda_db(lda_db.orignalDataConf.oid > 0).select()
    return dict(breadcrumb=['数据源配置管理','数据源配置'], panelTitle='基本信息',data = data)

def oringalEdit():
    data = lda_db(lda_db.orignalDataConf.oid == request.vars.id).select()
    return response.json(dict(data = data))

def orignalDelete():

    if  lda_db(lda_db.orignalDataConf.oid == request.vars.id).delete():
       ok = 0
    else:
        ok = 1
    return response.json(dict(data = ok))
    
     

def edit():
    try:
        if request.vars.status == "不选中":
            s ="no"
        elif  request.vars.status == "选中":
            s = "yes"
    except:    
            s = "no"
    lda_db(lda_db.orignalDataConf.oid == request.vars.ids).update(name=request.vars.dataName,
                                  dbEngine = request.vars.dbEngine,
                                  dbUser = request.vars.dbUser,
                                  dbPwd = request.vars.dbPwd,
                                  status = s,
                                  host= request.vars.ip,
                                  port = request.vars.port,
                                  dbName = request.vars.dbName,
                                  tableName = request.vars.tableName)
    redirect(URL('orignalData','orignalIndex'))


def getStatus():
    s = 3
    count = lda_db(lda_db.orignalDataConf.status == request.vars.statu).count()
    if count >= 1:
        s = 1
    if request.vars.id:
        dataStatus = lda_db(lda_db.orignalDataConf.oid == request.vars.id).select(lda_db.orignalDataConf.status).first()
        if dataStatus.status == "yes":
            s = 2
        else:
            s = 0
    return response.json(dict(data = s))
    
    
   
