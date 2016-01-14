class INDEX(object):
    def GET(self):
        '''
        if type(app) == 'str':
            pass
        else:
            app.start_response(app.status200,app.respheader)
        '''

        return "index\n"

class HELLO(object):
    def GET(self):
        return "hello\n"

class ROOT(object):
    def GET(self):
        return "root\n"
