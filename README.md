
# 📝 Backend - Lista de Tareas con Flask y SQL Server

## Descripción
Este proyecto implementa el **backend** de una aplicación de lista de tareas con usuarios, login y registro.  
Permite manejar tareas asociadas a cada usuario mediante una **API REST**, trabajando junto con un frontend independiente.  

El backend fue desarrollado en **Python con Flask** y conectado a **SQL Server**.

---

## Tecnologías utilizadas
- **Python 3.13** → lenguaje principal.  
- **Flask** → framework para crear la API REST.  
- **Flask-CORS** → permite comunicación con el frontend desde otro dominio/puerto.  
- **pyodbc** → librería para conectarse a SQL Server.  
- **SQL Server Express** → base de datos para usuarios y tareas.  


👉 Estas tecnologías fueron elegidas **principalmente** por poseer cierto **dominio** previo de las mismas, ademas de buena **compatibilidad con proyectos pequeños/medianos** y la facilidad de integrarse con SQL Server.  


---

## Instalación y configuración

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/Ferjud/backend.git
   cd backend-tareas
   
Ó
   
Copiar y pegar los códigos de cada archivo del repositorio Backend manualmente.



2. **Instalar dependencias**  
   ```bash
   pip install flask flask-cors pyodbc
   
3. **Configurar SQL Server**  
- **Abrir gestor de SQL Server(SSMS o Azure)**
- **Ejecutar el script SQL "Creación_ListaTares.sql" ubicado en el repositorio Backend**
- **En esta parte del código Python, cambiar el servidor SQL al de tu ordenador:
  ```bash
  conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=TU_SERVIDOR;"  
    "DATABASE=ListaTareas;"
    "Trusted_Connection=yes;" )
 
---

## Uso

- Luego de clonar o copiar los archivos de los repositorios Backend y Frontend, ejecutar app.py desde Pycharm(preferentemente), haciendo correr el código o desde la terminal del ordenador mediante:
  ```bash
  cd ruta/del/backend
 
Copiando luego la dirección del servidor en un navegador para visualizar la página.  