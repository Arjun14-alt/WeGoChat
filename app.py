from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "wegochat-secret-key"

# ✅ Render + SocketIO safe config
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


# -------------------------
# SOCKET EVENTS
# -------------------------

@socketio.on("join")
def handle_join(data):
    name = data["name"]
    room = data["room"]

    join_room(room)
    send({"msg": f"💬 {name} joined the chat"}, room=room)


@socketio.on("message")
def handle_message(data):
    room = data["room"]
    msg = data["msg"]
    name = data["name"]

    send({"msg": f"{name}: {msg}"}, room=room)


@socketio.on("leave")
def handle_leave(data):
    name = data["name"]
    room = data["room"]

    leave_room(room)
    send({"msg": f"🚪 {name} left the chat"}, room=room)


# -------------------------
# RUN (IMPORTANT FOR RENDER)
# -------------------------

if __name__ == "__main__":
    print("🔥 WeGoChat running...")
    socketio.run(
        app,
        host="0.0.0.0",
        port=10000
    )