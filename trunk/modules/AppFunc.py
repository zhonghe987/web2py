#coding:utf8


def show(data):
    if data == "user":
        s =  "用户"
    elif data == "admin":
        s = "管理员"
    elif data == "visit":
        s =  "访客"
    else:
        s = ''
    return s
    
def status(data):
    if data == "0":
        s =  '激活'
    elif data == "1":
        s =  '冻结'
    else:
        s = ''
    return s
        