#coding:utf8
LIMIT = 10

@auth.requires_login()
def index():
    import math
    breadcrumb = ['标签类别管理']
    bigData = [(name.l_id,name.bigName) for name in letv_db().select(letv_db.bigClass.l_id,letv_db.bigClass.bigName) ]
    bigData.insert(0, (0, '全部'))
    midData = [(name.cr_id,name.midName) for name in letv_db().select(letv_db.midClass.cr_id,letv_db.midClass.midName) ]
    midData.insert(0, (0, '全部'))
    btn = INPUT(_value='搜索',_type='submit',_id='subt')
    form =  SQLFORM.factory(
                                  Field('keyname'),
                                  Field('big',requires = IS_IN_SET(bigData)),
                                  Field('mid',requires = IS_IN_SET(midData)),
                                  buttons = [btn]
                                  )

    bcCondition = (letv_db.bigClass.id>0)
    mcCondition = (letv_db.midClass.id>0)
    #print request.post_vars
    if form.accepts(request, session):
        if request.post_vars.big != '0':
            bcCondition = (letv_db.bigClass.id == request.post_vars.big)
            mcCondition = (letv_db.midClass.b_id==request.post_vars.big)

        if request.post_vars.mid != '0':
            mcCondition = (letv_db.midClass.id==request.post_vars.mid)
            bcCondition = (letv_db.bigClass.id==0)

        if request.post_vars.keyname:            
            bcCondition = bcCondition & (letv_db.bigClass.bigName.like('%%%s%%'%request.post_vars.keyname))
            mcCondition = mcCondition & (letv_db.midClass.midName.like('%%%s%%'%request.post_vars.keyname))

    #print bcCondition
    bigClassData = letv_db(bcCondition).select()
    midClassData = letv_db(mcCondition).select(join=letv_db.bigClass.on(letv_db.bigClass.id==letv_db.midClass.b_id))
    bc = len(bigClassData)
    mc = len(midClassData)
    pageCount = int(math.ceil((bc+mc) / LIMIT))
    return dict(breadcrumb = breadcrumb,
                          form = form,
                          bigClassCount = bc,
                          bigClassData = bigClassData,
                          midClassCount =mc,
                          midClassData = midClassData,
                          pageCount = pageCount,
                         )



def splitPage():
    count  = int(request.vars.count - 1)  * LIMIT
    if request.vars.keyname:
       csdn =  csdn & (letv_db.lableClass.className.like('%%%s%%'%request.vas.name))
    if requset.vars.big:
       csdn = csdn & (letv_db.lableClass.l_id == request.vars.big)
    if request.vars.mid:
       csdn = csdn & (letv_db.lableClass.l_id == request.vars.mid)
    data = letv_db(csdn).select(letv_db.lableClass.className,letv_db.lableClass.classType,orderby = letv_db.lableClass.l_id,limitby = (count,count + LIMIT) )
    import  gluon.contrib.simplejson
    return resonse.json(dict(data = data))


@auth.requires_login()
def edit():
    breadcrumb = ['标签类别管理','新增标签类别']
    bigData = [(0,'--------')]
    bigData.extend([(items.l_id,items.bigName) for items in letv_db().select(letv_db.bigClass.bigName,letv_db.bigClass.l_id,orderby = letv_db.bigClass.l_id)])
    btn_sub = INPUT(_value='保存',_type='submit',_id='subt')
    btn_cnl  = INPUT(_value='取消',_type='button',_id='cancel')
    form = SQLFORM.factory(Field('mid_name',requires = IS_NOT_EMPTY()),
                                                      Field('big_name',requires = IS_IN_SET(bigData)),
                                                      Field('log_mark'),
                                                      buttons = [btn_sub, btn_cnl]
                                                     )
    if form.accepts(request,session):
        if request.post_vars.big_name == '0':
            letv_db.bigClass.insert(bigName=request.post_vars.mid_name, b_mark=request.post_vars.log_mark)
        else:           
            letv_db.midClass.insert(b_id = request.vars.big_name,midName = request.vars.mid_name,m_mark = request.vars.log_mark)

        redirect(URL('tagClassManage','index'))
    return dict(form  = form,breadcrumb  = breadcrumb )



def classDelete():
    import  gluon.contrib.simplejson
    mt_status = 202#(有标签，有小类)
    t_status = 101#（有标签）
    m_status = 606#（有小类）
    if request.vars.tag == '0':
        mId = [(m.cr_id,m.midName) for m in letv_db(letv_db.midClass.b_id == request.vars.id).select(letv_db.midClass.cr_id,letv_db.midClass.midName)]
        ids = {}
        vc= []
        if mId:
            for id,v in mId:
                tagDatas = [t.tagName for t in letv_db(letv_db.tagSource.midClass_id == id).select(letv_db.tagSource.tagName) ]
                vs = map(changeList,tagDatas)
                vc.append(v)
                if vs:
                    ids[v] = vs
            vv = map(changeList,vc)
            if not  ids:
                return response.json(dict(mId = vv,status = m_status))
            return response.json(dict(mId = ids,status = mt_status))
        letv_db(letv_db.bigClass.l_id == request.vars.id).delete()
        return 200
    if request.vars.id == '0':
        tag_id = [t.tagName for t in letv_db(letv_db.tagSource.midClass_id == request.vars.tag).select(letv_db.tagSource.tagName)]
        if tag_id:
            tag = map(changeList,tag_id)
            return response.json(dict(mId = tag,status = t_status))
        letv_db(letv_db.midClass.cr_id == request.vars.tag).delete()
        return 200
        
def changeList(lis):
        lis =' ' + lis
        return lis
                 
   
    
    
        
    
 
        
    
    
    
        
        
        
            
        
        
    
            
            
       