from sqlalchemy import Column, Integer, String, Boolean
import db

class Tarea(db.Base):  # Con Base, mapeamos nuestra clase con la base de datos
    ### Escribimos aquí la configuracion del ORM:
    __tablename__ = "tarea"  # Minúscula y singular
    # Para garantizar que el valor de la clave primaria, sea unico y nunca se reutilice por cada tabla:
    __table_args__ = {"sqlite_autoincrement": True}
    # Y aquí configurar las columnas:
    id = Column(Integer, primary_key=True)  # Automáticamente se convierte en autoincremental
    categoria = Column(String(60), nullable=False, default="Desconocido")
    contenido = Column(String(200), nullable=False)  # No puede haber nulos
    hecha = Column(Boolean, default=False)  # Si no pongo edad, escribe un -1
    fecha = Column(String(17), nullable=False, default="Infinito")

    ### ---------------------------------------------------------------------------

    def __init__(self, categoria, fecha, contenido, hecha):
        self.categoria = categoria
        self.fecha = fecha
        self.contenido = contenido
        self.hecha = hecha

    def __str__(self):
        return f"Tarea {self.id} | {self.categoria}: {self.contenido} hasta {self.fecha} | --> {self.hecha})"
