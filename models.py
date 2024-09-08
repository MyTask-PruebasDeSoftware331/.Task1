from datetime import datetime

class Tarea:
    def __init__(self, id, titulo, descripcion, etiqueta1, etiqueta2, venc_date, status, user_id):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.etiqueta1 = etiqueta1
        self.etiqueta2 = etiqueta2
        self.venc_date = venc_date
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo='{self.titulo}', status='{self.status}', etiqueta1='{self.etiqueta1}', etiqueta2='{self.etiqueta2}', user_id={self.user_id})>"

class User:
    def __init__(self, id, nombre, hashed_password):
        self.id = id
        self.nombre = nombre
        self.password = hashed_password

    def __repr__(self):
        return f"<User(id={self.id}, nombre='{self.nombre}')>"