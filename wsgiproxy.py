from wsgiref.simple_server import make_server
from application import class_my_app

httpd = make_server('',8086,class_my_app)
sa = httpd.socket.getsockname()
print 'http://{0}:{1}/'.format(*sa)
#print httpd.get_app()

httpd.serve_forever()
