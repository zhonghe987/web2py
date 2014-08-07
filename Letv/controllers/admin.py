#coding:utf-8

def login():
    form = auth.login()
    return dict( form = form)


def register():
    if  auth.is_logged_in():
       auth.logout(next = 'register')
    form = auth.register()
    return dict(form = form)


def logout():
    if  auth.is_logged_in():
        auth.logout()