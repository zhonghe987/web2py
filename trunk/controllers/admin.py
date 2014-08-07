#coding:utf-8


LIMIT = 10

def __addGroup(classes,ids):
    g_id = auth.id_group(classes)
    if not g_id:
        g_id = auth.add_group(classes, classes)
    auth.add_membership(g_id, ids)
    return



def __judgeuser(form):
    if auth.user.status != "0":
        redirect(URL('default','index'))
    else:
        redirect(URL('default','errorPage'))
    

def __getClasses():
    c = tag_db(tag_db.auth_user.id == auth.user.id).select(tag_db.auth_user.classes,tag_db.auth_user.status).first()
    return auth.user and 'admin' == c.classes and '1' == c.status 

def check():
    data = dict([(k.username,k.showPass) for k in tag_db(tag_db.auth_user.id >0).select(tag_db.auth_user.username,tag_db.auth_user.showPass)])
    s = data.get(request.vars.username,None) 
    if not s:
        return response.json(dict(result=1))
    if s != request.vars.password:
        return response.json(dict(result=1))
    return response.json(dict(result=0))   


def login():
    s =  tag_db(tag_db.auth_user.first_name == 'admin').select(tag_db.auth_user.id).first()
    if not s:
        import time
        auth.register_bare(username="admin",password = "admin001",
                       datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),
                       showPass = "admin001",classes = "admin",
                       company = "",chinaName = "admin",
                       status = "1",
                       depart = "master" )
        ids = tag_db(tag_db.auth_user.username=='admin').select(tag_db.auth_user.id).first().id
        __addGroup('admin',ids)
    form = auth.login(onaccept = __judgeuser)
    return dict( form = form)


def register():
    if  auth.is_logged_in():
        auth.logout(next="register")
    form = auth.register()
    return dict(form = form)

def logout():
    if  auth.is_logged_in():
        auth.logout(next="login")

        


@auth.requires(__getClasses,requires_login=True)
def  userManage():
    import math
    import gluon.contrib.simplejson as sj
    classes = [('all','全部'),("admin",'管理员'),("user",'用户'),('visit','访客')]  
    breadcrumb = ['用户管理']
    btn = INPUT(_value='搜索',_type='submit',_id='subt')
    con = {'classes':'all','username':'','name':'','idList':''}
    form = SQLFORM.factory(Field('username'),
                           Field('name'),
                           Field('classes',requires = IS_IN_SET(classes)),
                           buttons = [btn])
    csdn = (tag_db.auth_user.id > 0)
    if form.accepts(request,session):
        if request.vars.classes != "all":
            csdn = csdn & (tag_db.auth_user.classes == request.vars.classes )
            con['classes'] = request.vars.classes
        if request.vars.username != '':
            csdn = csdn & (tag_db.auth_user.username.like('%%%s%%'%request.vars.username))
            con['username'] = request.vars.username
        if request.vars.name != '':
            con['name'] = request.vars.name
            csdn = csdn & (tag_db.auth_user.chinaName.like('%%%s%%'%request.vars.name))   
    data = tag_db(csdn).select(tag_db.auth_user.id,
                                                  tag_db.auth_user.username,
                                                  tag_db.auth_user.chinaName,
                                                  tag_db.auth_user.classes,
                                                  tag_db.auth_user.datetime,
                                                  tag_db.auth_user.status,
                                                  orderby  = tag_db.auth_user.classes
                                                  )
    
    count = len(data)
    pagCount =  int(math.ceil(float(count) / LIMIT))
    tenData = data[:LIMIT]
    con['idList'] = sj.dumps([k.id for k in tenData])
    return dict(breadcrumb = breadcrumb,datas = tenData,form = form,count = count,pageCount = pagCount,find = con)



def backData():
    import gluon.contrib.simplejson as sj
    csdn = (tag_db.auth_user.id > 0)
    if request.vars.classes != "all":
            csdn = csdn & (tag_db.auth_user.classes == request.vars.classes )
    if request.vars.username != '':
            csdn = csdn & (tag_db.auth_user.username.like('%%%s%%'%request.vars.username))
    if request.vars.name != '':
            csdn = csdn & (tag_db.auth_user.chinaName.like('%%%s%%'%request.vars.name))
    startId = (int(request.post_vars.page)-1) * LIMIT
    data =  tag_db(csdn).select(tag_db.auth_user.id,
                                tag_db.auth_user.username,
                                tag_db.auth_user.chinaName,
                                tag_db.auth_user.classes,
                                tag_db.auth_user.datetime,
                                tag_db.auth_user.status,
                                limitby = (startId,startId + LIMIT),
                                orderby = tag_db.auth_user.classes).as_list()
                                
    con =sj.dumps( [k['id'] for k in data])
    
    return response.json(dict(data=data, startId=startId+1,con = con))



@auth.requires(__getClasses ,requires_login=True) 
def freeze():
    if len(request.vars.status)> 1:
        tag_db.executesql("update  auth_user set status='0'  where id in  (%s)"%(request.vars.status[:-1]))
        s =  '%s,'%request.vars.ids[1:-1]
        data = tag_db(tag_db.auth_user.id.belongs((s))).select(tag_db.auth_user.id,
                                                                                           tag_db.auth_user.username,
                                                                                           tag_db.auth_user.chinaName,
                                                                                           tag_db.auth_user.classes,
                                                                                           tag_db.auth_user.datetime,
                                                                                           tag_db.auth_user.status,
                                                                                           orderby=tag_db.auth_user.id)
        return response.json(dict(data=data))
    else:
        if request.vars.status == '1':
            tag_db(tag_db.auth_user.id == request.vars.id).update(status = '0')
            data =  '0'
        elif request.vars.status == '0':
            tag_db(tag_db.auth_user.id == request.vars.id).update(status = '1')
            data =  '1'
        return data
    



@auth.requires(__getClasses ,requires_login=True) 
def addUser():
    import time
    btn = INPUT(_value='保存',_type='submit',_id='subt')
    classes = [("admin",'管理员'),("user",'用户'),('visit','访客')]            
    breadcrumb = ['用户管理','新增管理']
   
    form  = SQLFORM.factory(Field('classes',requires = IS_IN_SET(classes)),
                            Field('username',requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(tag_db,'auth_user.username') ]),
                            Field('password',requires = IS_NOT_EMPTY()),
                            Field('chinaName'),
                            Field('company',requires = IS_NOT_EMPTY()),
                            Field('depart'),
                            buttons = [btn]
                            )
    
    if form.accepts(request,session):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        auth.register_bare(username = request.vars.username,password = request.vars.password,
                           classes = request.vars.classes,chinaName = request.vars.chinaName,
                           company = request.vars.company, depart = request.vars.depart,showPass = request.vars.password,
                           datetime = datetime,status = '1')
        ids = tag_db(tag_db.auth_user.username == request.vars.username).select(tag_db.auth_user.id).first()
        __addGroup(request.vars.classes,ids.id)
        redirect(URL('admin','userManage'))
    return dict(breadcrumb = breadcrumb,form = form)



@auth.requires(__getClasses ,requires_login=True) 
def editUser():
    import time
    btn = INPUT(_value='保存',_type='submit',_id='subt')
    classes = [("admin",'管理员'),("user",'用户'),('visit','访客')]  
    breadcrumb = ['用户管理','编辑管理']
    data = tag_db(tag_db.auth_user.id == request.vars.eid).select(
                                                  tag_db.auth_user.id,
                                                  tag_db.auth_user.username,
                                                  tag_db.auth_user.chinaName,
                                                  tag_db.auth_user.classes,
                                                  tag_db.auth_user.company,
                                                  tag_db.auth_user.depart,
                                                  tag_db.auth_user.showPass
                                                  ).first()
    
    form = SQLFORM.factory(
                            Field('classes',requires = IS_IN_SET(classes)),
                            Field('username',requires = IS_NOT_EMPTY() ),
                            Field('password',requires = IS_NOT_EMPTY()),
                            Field('chinaName',requires = IS_NOT_EMPTY()),
                            Field('company',requires = IS_NOT_EMPTY()),
                            Field('depart',requires = IS_NOT_EMPTY()),
                            buttons = [btn]
                           )
        
    if form.accepts(request,session):
            upList = ['classes','username','password','chinaName','company','depart','showPass']
            from gluon.validators import  CRYPT
            alg = 'pbkdf2(1000,20,sha512)'
            datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            tag_db(tag_db.auth_user.id == data.id).update(
                                                          username = request.vars.username,showPass =request.vars.password,
                   password=str(CRYPT(digest_alg=alg,salt=True)(request.vars.password)[0]),
                           classes = request.vars.classes,
                           chinaName = request.vars.chinaName,
                           company = request.vars.company,
                           depart = request.vars.depart,
                           datetime = datetime,status = '1'
                                                          )
            
            __addGroup(request.vars.classes,data.id)
            classes = tag_db(tag_db.auth_user.id == auth.user.id).select(tag_db.auth_user.classes).first().classes
            if classes == "admin":
                redirect(URL('admin','userManage'))
            else:
                redirect(URL('admin','login'))
      
    return dict(breadcrumb = breadcrumb,data = data,form = form)
