from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "wegotchat-secret"

# ✅ IMPORTANT: no eventlet, no gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


# 💬 Join room
@socketio.on("join")
def handle_join(data):
    name = data["name"]
    room = data["room"]

    join_room(room)
    send({"msg": f"💬 {name} joined the chat"}, room=room)


# 💬 Message handler
@socketio.on("message")
def handle_message(data):
    room = data["room"]
    msg = data["msg"]
    name = data["name"]

    send({"msg": f"{name}: {msg}"}, room=room)


# 💬 Leave room
@socketio.on("leave")
def handle_leave(data):
    name = data["name"]
    room = data["room"]

    leave_room(room)
    send({"msg": f"🚪 {name} left the chat"}, room=room)


# 🚀 RUN SERVER (THIS IS CRITICAL)
if __name__ == "__main__":
    print("🔥 WeGoChat starting...")
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)