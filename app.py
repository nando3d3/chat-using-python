from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, emit, SocketIO
import random
from string import ascii_uppercase

import cv2
import base64
import io
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

rooms = {}
predefined_themes = ["Música", "Engenharia", "Esportes", "Dança", "Video Game"]

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/", methods=["POST", "GET"])
def home():
  session.clear()
  if request.method == "POST":
      name = request.form.get("name")
      theme = request.form.get("theme")
      join = request.form.get("join", False)

      if not name:
          return render_template("home.html", error="Please enter a name.", name=name, themes=predefined_themes)

      if theme in predefined_themes:
          room = theme
          if room not in rooms:
              rooms[room] = {"members": 0, "messages": []}
          session["room"] = room
          session["name"] = name
          return redirect(url_for("room"))

      if join != False:
          code = request.form.get("code")
          if not code:
              return render_template("home.html", error="Please enter a room code.", name=name, themes=predefined_themes)

          room = code
          if code not in rooms:
              return render_template("home.html", error="Room does not exist.", code=code, name=name, themes=predefined_themes)
      else:
          return render_template("home.html", error="Invalid theme.", name=name, themes=predefined_themes)

  return render_template("home.html", themes=predefined_themes)

@app.route("/room")
def room():
   room = session.get("room")
   if room is None or session.get("name") is None:
       return redirect(url_for("home"))

   if room not in rooms:
       # Verifica se o código da sala é um tema
       if room in predefined_themes:
           rooms[room] = {"members": 0, "messages": []}
       else:
           return redirect(url_for("home"))

   return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

@socketio.on('image')
def image(data_image):
    sbuf = io.StringIO()
    sbuf.write(data_image)
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame = cv2.flip(frame, flipCode=0)
    imgencode = cv2.imencode('.jpg', frame)[1]

    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)