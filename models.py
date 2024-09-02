# models.py

from datetime import datetime

class Tarea:
    def __init__(self, id, titulo, descripcion, etiqueta, venc_date, pendiente, in_progress, completado, archivado, user_id):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.etiqueta = etiqueta
        self.venc_date = venc_date
        self.pendiente = pendiente
        self.in_progress = in_progress
        self.completado = completado
        self.archivado = archivado
        self.user_id = user_id

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo='{self.titulo}', user_id={self.user_id})>"

class User:
    def __init__(self, id, nombre, hashed_password):
        self.id = id
        self.nombre = nombre
        self.password = hashed_password  # This is now a hashed password

    def __repr__(self):
        return f"<User(id={self.id}, nombre='{self.nombre}')>"