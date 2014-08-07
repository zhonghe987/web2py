# -*- coding: utf-8 -*-
 
def __addGroup(form):
    g_id = auth.id_group(auth.user.company)
    if not g_id:
        g_id = auth.add_group(auth.user.company, auth.user.company)
    auth.add_membership(g_id, auth.user.id)
    return

def __judgeAdmin(form):
   print 'judge admin:',auth.user
   if auth.user.company == 'admin':
       redirect(URL('schedule'))

def login():
    form = auth.login(onaccept=__judgeAdmin)
    return dict(form=form,errors = "")


def register():
    if auth.is_logged_in():
        auth.logout(next="register")
    forms = auth.register(onaccept=__addGroup)
    return dict(form=forms)


def logout():
    if  auth.is_logged_in():
        auth.logout()

@auth.requires_membership('admin')
def schedule():
    task = sch_db(sch_db.scheduler_task.task_name=='updateDataSource').select(orderby='id desc').first()
    status = 'COMPLETED'
    taskId = 0
    stopTime = '-'
    if task:
        status = task.status
        taskId = task.id
        tr = sch_db(sch_db.scheduler_run.task_id==taskId).select(orderby='id desc').first()
        stopTime = tr.stop_time
    return dict(breadcrumb=['计划任务管理'], panelTitle='',task=task, status=status, taskId=taskId, stoptime=stopTime) 

@auth.requires_membership('admin')
def taskAction():
    print 'task action:', request.post_vars
    if request.post_vars.act == 'start':
        task = scheduler.queue_task('updateDataSource', 
                                                                 repeats=int(request.post_vars.repeats), 
                                                                 period=int(request.post_vars.period),
                                                                 timeout=86400)
        act = 'stop'
        des = '暂停'
        taskId = task.id
    elif request.post_vars.act == 'stop':
        act = 'start'
        des = '启动'
        taskId = 0
        #scheduler.stop_task(request.post_vars.taskId)
        sch_db(sch_db.scheduler_task.id==request.post_vars.taskId).update(status='STOPPED');
    return response.json(dict(act=act, des=des, taskId=taskId))

@auth.requires_membership('admin')
def taskInfo():
    taskId = request.post_vars.taskId
    task = sch_db(sch_db.scheduler_task.id==taskId).select().first()
    print 'task info', task.status
    stoptime = '-'
    if task.status == 'COMPLETED' or task.status == 'FAILED':
        tr = sch_db(sch_db.scheduler_run.task_id==taskId).select(orderby='id desc').first()
        stoptime = tr.stop_time    
    return response.json(dict(task=task, stoptime=stoptime));