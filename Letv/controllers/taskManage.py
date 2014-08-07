#coding:utf-8

@auth.requires_login()
def index():
    task = sch_db(sch_db.scheduler_task.task_name=='tagProcess').select(orderby='id desc').first()
    #print 'task', task
    if task:
        status = task.status
        taskId = task.id
    else:
        status = 'COMPLETED'
        taskId = 0
   
    return dict(breadcrumb = ['任务管理'], task=task, status=status, taskId=taskId)


def taskAction():
    #print 'task action:', request.post_vars
    if request.post_vars.act == 'start':
        import os
        import datetime
        p = os.path.join(request.folder, 'private')
        pvars=dict(filename=os.path.join(p,'20140522.txt'), savefile=os.path.join(p, 'result-%s.txt' %datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        task = scheduler.queue_task('tagProcess', pvars=pvars, timeout=86400)
        act = 'stop'
        des = '暂停'
        taskId = task.id
    elif request.post_vars.act == 'stop':
        act = 'start'
        des = '启动'
        taskId = 0

    return response.json(dict(act=act, des=des, taskId=taskId))


def taskInfo():
    task = sch_db(sch_db.scheduler_task.id==request.post_vars.taskId).select().first()
    print 'task info', request.post_vars.taskId, task.status
    return response.json(dict(task=task));


