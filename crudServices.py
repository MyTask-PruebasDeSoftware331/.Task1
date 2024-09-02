# crud_services.py
import bcrypt
from database import get_db_connection
from models import Tarea, User
from datetime import datetime


# User services
def create_user(nombre, password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cur.execute('INSERT INTO USER (nombre, password) VALUES (?, ?)', (nombre, hashed_password))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def get_user(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM USER WHERE nombre = ?', (nombre,))
    user_data = cur.fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['nombre'], user_data['password'])
    return None

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Tarea services
def create_tarea(titulo, descripcion, etiqueta, venc_date, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO TAREAS (titulo, descripcion, etiqueta, venc_date, pendiente, in_progress, completado, archivado, user_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, etiqueta, venc_date, True, False, False, False, user_id))
    conn.commit()
    tarea_id = cur.lastrowid
    conn.close()
    return tarea_id

def read_tarea(tarea_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM TAREAS WHERE id = ?', (tarea_id,))
    tarea_data = cur.fetchone()
    conn.close()
    if tarea_data:
        return Tarea(**tarea_data)
    return None

def update_tarea(tarea_id, titulo, descripcion, etiqueta, venc_date, pendiente, in_progress, completado, archivado):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE TAREAS 
        SET titulo = ?, descripcion = ?, etiqueta = ?, venc_date = ?, 
            pendiente = ?, in_progress = ?, completado = ?, archivado = ?
        WHERE id = ?
    ''', (titulo, descripcion, etiqueta, venc_date, pendiente, in_progress, completado, archivado, tarea_id))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

def delete_tarea(tarea_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM TAREAS WHERE id = ?', (tarea_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

def list_tareas(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM TAREAS WHERE user_id = ?', (user_id,))
    tareas_data = cur.fetchall()
    conn.close()
    return [Tarea(**t) for t in tareas_data]