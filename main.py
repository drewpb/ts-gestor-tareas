from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

app = Flask(__name__)

@app.route("/")
def home():
    tareas_db = db.session.query(Tarea).all()
    print(tareas_db)
    for t in tareas_db:
        print(t)
    return render_template("index.html", lista_tareas=tareas_db)

# Para tener la capacidad de poder enviar información --> methods["POST"]
@app.route("/crear-tarea", methods= ["POST"])  # Cuando se acceda a esta URL
def crear():  # Se ejecutará esta funcion
    # print(f"Creando tarea.. {request.form["contenido_categoria"]} ; {request.form["contenido_fecha"]} ; {request.form["contenido_tarea"]} ; ")
    tarea = Tarea(categoria=request.form["contenido_categoria"], fecha=request.form["contenido_fecha"], contenido=request.form["contenido_tarea"], hecha=False)  # Al crear una tarea, por defect no están hecha
    print(tarea)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")  # Cuando se acceda a esta URL se pasará el id del objeto
def hecha(id):  # Se ejecutará esta funcion
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    tarea.hecha = not(tarea.hecha)
    # print(f"HECHA!!: {tarea}")
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/borrar-tarea/<id>")  # Cuando se acceda a esta URL se pasará el id del objeto
def borrar(id):  # Se ejecutará esta funcion
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/editar-tarea/<id>")  # Cuando se acceda a esta URL se pasará el id del objeto
def editar(id):  # Se ejecutará esta funcion
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    return render_template("edit.html", tarea_edit=tarea)

# Cuando se acceda a esta URL se pasará el id del objeto
@app.route("/editar-tarea/<id>/ok", methods= ["POST"])
def editar_ok(id):  # Se ejecutará esta funcion
    # print(f"Editando tarea.. {request.form["contenido_categoria"]} ; {request.form["contenido_fecha"]} ; {request.form["contenido_tarea"]} ; ")
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    tarea.contenido = request.form["contenido_tarea"]
    tarea.fecha = request.form["contenido_fecha"]
    tarea.categoria = request.form["contenido_categoria"]
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    from os import getenv
    
    # Esto va a ir al fichero db.py, poner en marcha todo lo que tenemos ahi, llegar al
    # fichero models, poner en marcha todo y mapear las clases.
    db.Base.metadata.create_all(db.engine)

    port = int(getenv("PORT", 5000))  # Render asigna un puerto dinámico
    app.run(host="0.0.0.0", port=port)
""" POSIBLES ERRORES:
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
- SOLUCION:
1. Identificar el proceso que está usando el puerto 5000: 'sudo lsof -i :5000'
2. Detener el proceso: 'sudo kill -9 PID'
"""