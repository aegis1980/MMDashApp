from baseapp import app as baseapp

from flask_sockets import Sockets

sockets = Sockets(app)

@sockets.route('/api')
def api(ws):
    while not ws.closed:
        message = ws.receive()
        data = json.loads(message)
        print(message)
        echo = data['msg']
        ws.send(echo)