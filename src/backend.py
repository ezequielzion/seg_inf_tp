from flask import Flask, request, make_response, render_template, redirect
import queue
from generadores import generadores
import uuid
import os

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


def sanitizar_contenido(contenido: str) -> str:
    # implementar!!!!
    # quizas esto ayude https://flask.palletsprojects.com/en/3.0.x/quickstart/#html-escaping
    return contenido


def persistir_token(contenido: str) -> str:
    id = str(uuid.uuid4())
    with open("tokens-generados.txt", "a") as f:
        f.write(id + "\t" + contenido)
    return id


def generar_endpoint(id: str) -> str:
    return f"http://localhost:5000/alert/{id}"


announcer = MessageAnnouncer()

app = Flask(__name__)


@app.get("/")
def hello_world():
    return render_template('frontend.html')


@app.post("/nuevoToken")
def nuevo_token():
    body = request.get_json()
    tipo = body["tipo"]
    if tipo not in generadores:
        raise ValueError("el tipo de token no está soportado")

    contenido = sanitizar_contenido(body["contenido"])
    id = persistir_token(contenido)
    endpoint = generar_endpoint(id)
    return generadores[tipo](endpoint)


@app.get("/listen")
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield "data: " + msg + "\n\n"

    response = make_response(stream())
    response.headers["Mimetype"] = "text/event-stream"
    response.headers["Content-Type"] = "text/event-stream"
    return response


@app.get("/alert/<uuid:id>")
def alert(id: uuid):
    contenido = None
    id_str = str(id)
    with open("tokens-generados.txt", "r+") as f:
        for line in f:
            parts = line.split("\t")
            if parts[0] == id_str:
                contenido = parts[1]
                if not contenido:
                    contenido = ""
                break

    if contenido == None:
        # alertar al admin o a alguien que se intento llamar al alert con un id falso, alguien descubrio el endpoint
        pass
    else: 
        announcer.announce(contenido)
        
    return ("informa3", 200)

@app.route('/redirect')
def redirect_route():
    final_url = request.args.get('final_url')
    response = redirect(final_url, code=302)
    return response

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
