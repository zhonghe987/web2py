#coding:utf-8

from gluon.tools import Auth
letv_db = DAL('mysql://idexadmin:idex000@180.169.19.150/Letv')
#letv_db = DAL('mysql://root:root@127.0.0.1/Letv')

auth = Auth(letv_db)
auth.define_tables(username=True, migrate=False)
auth.settings.controller = 'admin'
auth.settings.login_url = URL('admin','login')
auth.settings.logged_url = URL('tagManage','index')
auth.settings.login_next = URL('tagManage','index')
auth.settings.register_next = URL('admin','login')
auth.settings.logout_next = URL('admin','login')

#规则
letv_db.define_table('rules',
                     Field('r_id','id'),
                     Field('col_name'),
                     Field('condition_op'),
                     Field('content'),
                     Field('createDate','date'),
                     )

#标签表
letv_db.define_table('tagSource',
                    Field('t_id','id'),
                    Field('bigClass_id','integer'),
                    Field('midClass_id','integer'),
                    Field('tagName'),
                    Field('createDate','date',default='CURRENT_DATE'),
                    )

#类别
letv_db.define_table('bigClass',
                     Field('l_id','id'),
                     Field('bigName'),
                     Field('b_mark'),
                     )

#规则组
letv_db.define_table('ruleGroup',
                     Field('rg_id','id'),
                     Field('tag_id','integer'),
                     Field('createDate','date'),
                     )



#规则与组的映射
letv_db.define_table('ruleFilterGroup',
                     Field('rfg_id','id'),
                     Field('rules_id','integer'),
                     Field('ruleGroup_id','integer'),
                     )


#类别关系表
letv_db.define_table('midClass',
                     Field('cr_id','id'),
                     Field('b_id','integer'),
                     Field('midName'),
                     Field('m_mark')
                     )

# 标签日志表
letv_db.define_table('tagLog',
                                          Field('tl_id','id'),
                                          Field('userId'),
                                          Field('tagId', 'integer'),
                                          Field('date', 'datetime')
)