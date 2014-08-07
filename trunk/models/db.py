#coding:utf-8

from datetime import datetime
from gluon.tools import Auth
tag_db = DAL('mysql://idexadmin:idex000@180.169.19.150/tagRuleAdmin',migrate_enabled=False)
T.force('zh-cn')
auth = Auth(tag_db)
auth.settings.controller = 'admin'
auth.settings.login_url = URL('admin','login')
auth.settings.expiration = 3600
auth.settings.logout_next = URL('admin','login')
auth.settings.extra_fields['auth_user'] = [Field('status'),Field('showPass'),Field('classes'),Field('company'),Field('phone'),Field('depart'),Field('chinaName'),Field('datetime')]
auth.define_tables(username=True)

# 频道表
tag_db.define_table('ContentInfo',
                                          Field('c_id', 'id'),
                                          Field('channel',default=''),
                                          Field('album',default=''),
                                          Field('area',default=''),
                                          Field('site',default=''),
                                          Field('createDate','datetime')
                                          )


# 维度表
tag_db.define_table('Dimension',
                                          Field('d_id', 'id'),
                                          Field('name'),
                                          Field('symbol'),
                                          Field('dimDesc'),
                                          Field('status'),
                                          Field('createDate', 'datetime')
                                         )

# 元素表
tag_db.define_table('Element',
                                          Field('e_id', 'id'),
                                          Field('d_id', 'integer'),
                                          Field('name'),
                                          Field('symbol'),
                                          Field('eleDesc'),
                                          Field('status'),
                                          Field('dbCheck'),
                                          Field('createDate', 'datetime'),
                                         )

#标签表
tag_db.define_table('Tag',
                                          Field('t_id','id'),
                                          Field('name'),
                                          Field('json','text'),
                                          Field('company'),
                                          Field('status'),
                                          Field('tagDesc'),
                                          Field('createDate','datetime'),
                                          )


# 标签日志表
tag_db.define_table('TagPullLog',
                                          Field('tp_id','id'),
                                          Field('ip'),
                                          Field('count', 'integer'),
                                          Field('mode'),
                                          Field('startTagId', 'integer'),
                                          Field('company'),
                                          Field('createDate', 'datetime')
)
