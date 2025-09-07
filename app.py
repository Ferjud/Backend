from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import pyodbc

app = Flask(__name__)
app.secret_key = "secreto"
CORS(app)

# Carpeta del frontend
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")


# Conexión a SQL Server

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-BM44EOE\SQLEXPRESS;"  
    "DATABASE=ListaTareas;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()


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



# API REST con SQL Server


# Registro de usuario
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Verificar usuario existente
    cursor.execute("SELECT id FROM Usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "El usuario ya existe"})

    # Insertar usuario nuevo
    cursor.execute("INSERT INTO Usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

    return jsonify({"success": True, "message": "Registro exitoso, inicie sesión"})


# Login de usuario
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT id FROM Usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrecta"})

    session["usuario"] = username
    return jsonify({"success": True})


# Obtener / agregar tareas
@app.route("/api/tareas", methods=["GET", "POST"])
def manejar_tareas():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"success": False, "message": "No autorizado"})

    # Buscar id del usuario
    cursor.execute("SELECT id FROM Usuarios WHERE username = ?", (usuario,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"})
    usuario_id = user[0]

    if request.method == "POST":
        data = request.json
        texto = data.get("tarea")
        cursor.execute("INSERT INTO Tareas (usuario_id, descripcion) VALUES (?, ?)", (usuario_id, texto))
        conn.commit()
        return jsonify({"success": True})

    # GET: traer tareas del usuario
    cursor.execute("SELECT id, descripcion FROM Tareas WHERE usuario_id = ?", (usuario_id,))
    tareas = [{"id": row[0], "texto": row[1]} for row in cursor.fetchall()]
    return jsonify({"success": True, "tareas": tareas})


# Eliminar tarea
@app.route("/api/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"success": False, "message": "No autorizado"})

    # Buscar id del usuario
    cursor.execute("SELECT id FROM Usuarios WHERE username = ?", (usuario,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"})
    usuario_id = user[0]

    # Eliminar tarea
    cursor.execute("DELETE FROM Tareas WHERE id = ? AND usuario_id = ?", (id, usuario_id))
    conn.commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
