from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "secreto"
CORS(app)

# Carpeta del frontend
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")

# Simulación de base de datos
usuarios = {
    "fernando": "1234",
    "maria": "abcd",
    "juan": "pass123"
}

tareas = {
    "fernando": [],
    "maria": [],
    "juan": []
}

@app.route("/")
def login_page():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/home")
def home_page():
    return send_from_directory(FRONTEND_FOLDER, "home.html")


# Servir archivos estáticos del frontend (CSS, JS)
@app.route("/<path:archivo>")
def static_files(archivo):
    return send_from_directory(FRONTEND_FOLDER, archivo)



# API REST


# Registro de usuario
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in usuarios:
        return jsonify({"success": False, "message": "El usuario ya existe"})

    usuarios[username] = password
    tareas[username] = []
    return jsonify({"success": True, "message": "Registro exitoso, inicie sesión"})


# Login de usuario
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username not in usuarios:
        return jsonify({"success": False, "message": "Usuario incorrecto"})

    if usuarios[username] != password:
        return jsonify({"success": False, "message": "Contraseña incorrecta"})

    session["usuario"] = username
    return jsonify({"success": True, "message": "Login correcto"})


# Obtener / agregar tareas
@app.route("/api/tareas", methods=["GET", "POST"])
def manejar_tareas():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"success": False, "message": "No autorizado"})

    if request.method == "POST":
        data = request.json
        texto = data.get("tarea")
        id_tarea = len(tareas[usuario])
        tareas[usuario].append({"id": id_tarea, "texto": texto})
        return jsonify({"success": True})

    # GET
    return jsonify({"success": True, "tareas": tareas[usuario]})


# Eliminar tarea
@app.route("/api/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    usuario = session.get("usuario")
    if not usuario or id >= len(tareas[usuario]):
        return jsonify({"success": False})
    tareas[usuario].pop(id)
    # Reindexar IDs
    for i, t in enumerate(tareas[usuario]):
        t["id"] = i
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
