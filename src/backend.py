from flask import Flask, request, make_response
import queue

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

announcer = MessageAnnouncer()

app = Flask(__name__)

tipos = {
    "pdf",
    "excel",
    "word",
    "epub",
    "mysql",
}


@app.get("/")
def hello_world():
    with open("frontend.html", "r+") as f:
        return f.read()


@app.post("/nuevoToken")
def nuevoToken():
    body = request.get_json()
    print(body)
    if body["tipo"] not in tipos:
        raise ValueError("el tipo de token no está soportado")
    return "ok!"

@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield "data: " + msg + "\n\n"
    response = make_response(stream())
    response.headers['Mimetype'] = 'text/event-stream'
    response.headers['Content-Type'] = 'text/event-stream'
    return response


@app.get('/honey-token')
def post():
    announcer.announce(msg="se picó el token che")
    return ("informa3", 200)


app.run()
