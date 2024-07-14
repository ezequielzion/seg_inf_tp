from flask import Flask, request, make_response, render_template, redirect
import queue
from generadores import generadores
import uuid
import os
from markupsafe import escape
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('PORT', 5000))

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
    # quizas esto ayude https://flask.palletsprojects.com/en/3.0.x/quickstart/#html-escaping
    return escape(contenido)


def persistir_token(contenido: str) -> str:
    id = str(uuid.uuid4())
    with open("tokens-generados.txt", "a") as f:
        f.write(id + "\t" + contenido + "\n")
    return id


def generar_endpoint(id: str) -> str:
    return f"http://localhost:{PORT}/alert/{id}"

def generate_alert_with_uuid(id: str):
    print("generating alert", id)
    with open("tokens-generados.txt", "r+") as f:
        for line in f:
            parts = line.split("\t")
            if parts[0] == id:
                contenido = parts[1]
                if not contenido:
                    contenido = ""
                break

    if contenido == None:
        # alertar al admin o a alguien que se intento llamar al alert con un id falso, alguien descubrio el endpoint
        pass
    else: 
        announcer.announce(contenido)


announcer = MessageAnnouncer()

app = Flask(__name__)


@app.get("/")
def hello_world():
    return render_template('frontend.html')


@app.post("/nuevoToken")
def nuevo_token():
    body = request.get_json()
    userAgentData = body["userAgentData"]
    tipo = body["tipo"]
    contenido = body["contenido"]
    if tipo not in generadores:
        raise ValueError("el tipo de token no está soportado")

    contenido_sanitizado = sanitizar_contenido(contenido)
    id = persistir_token(contenido_sanitizado)
    endpoint = generar_endpoint(id)
    return generadores[tipo](endpoint, userAgentData)


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
    uuid = str(id)
    generate_alert_with_uuid(uuid)
    return ("informa3", 200)

@app.route('/redirect')
def redirect_route():
    final_url = request.args.get('final_url')
    uuid = request.args.get('endpoint').split('/')[-1]
    generate_alert_with_uuid(uuid)
    response = redirect(final_url, code=302)
    return response

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=PORT)
