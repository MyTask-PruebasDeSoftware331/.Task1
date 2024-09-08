import bcrypt
from database import get_db_connection
from models import Tarea, User
from datetime import datetime
from loggerSetup import db_logger, user_logger

def create_user(nombre, password):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if the username already exists
    cur.execute('SELECT * FROM USER WHERE nombre = ?', (nombre,))
    existing_user = cur.fetchone()
    
    if existing_user:
        conn.close()
        user_logger.warning(f"Usuario ya existente: {nombre}")
        return None  # Return None to indicate that the user creation failed
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cur.execute('INSERT INTO USER (nombre, password) VALUES (?, ?)', (nombre, hashed_password))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    user_logger.info(f"Nuevo usuario creado: {nombre}")
    return user_id

def get_user(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM USER WHERE nombre = ?', (nombre,))
    user_data = cur.fetchone()
    conn.close()
    if user_data:
        user_logger.info(f"User retrieved: {nombre}")
        return User(user_data['id'], user_data['nombre'], user_data['password'])
    user_logger.warning(f"Intento fallido de login para usuario: {nombre}")
    return None

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_tarea(titulo, descripcion, etiqueta1, etiqueta2, venc_date, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    status = 'Pendiente'
    if venc_date and venc_date < datetime.now():
        status = 'Vencido'
    venc_date_str = venc_date.strftime("%Y-%m-%d %H:%M:%S") if venc_date else None
    cur.execute('''
        INSERT INTO TAREAS (titulo, descripcion, etiqueta1, etiqueta2, venc_date, status, user_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, etiqueta1, etiqueta2, venc_date_str, status, user_id))
    conn.commit()
    tarea_id = cur.lastrowid
    conn.close()
    db_logger.info(f"Nueva tarea creada: ID {tarea_id}, Titulo '{titulo}', User ID {user_id}")
    return tarea_id

def update_tarea(tarea_id, titulo, descripcion, etiqueta1, etiqueta2, venc_date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT status FROM TAREAS WHERE id = ?', (tarea_id,))
    current_status = cur.fetchone()[0]
    status = current_status
    
    if venc_date:
        if venc_date > datetime.now():
            if status == 'Vencido':
                status = 'Pendiente'
        elif status not in ['Completado', 'Archivado']:
            status = 'Vencido'
    
    venc_date_str = venc_date.strftime("%Y-%m-%d %H:%M:%S") if venc_date else None
    cur.execute('''
        UPDATE TAREAS 
        SET titulo = ?, descripcion = ?, etiqueta1 = ?, etiqueta2 = ?, venc_date = ?, status = ?
        WHERE id = ?
    ''', (titulo, descripcion, etiqueta1, etiqueta2, venc_date_str, status, tarea_id))
    conn.commit()
    conn.close()
    db_logger.info(f"Tarea actualizada: ID {tarea_id}, Titulo '{titulo}'")
    return cur.rowcount > 0

def update_tarea_status(tarea_id, new_status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT status, venc_date FROM TAREAS WHERE id = ?', (tarea_id,))
    current_status, venc_date_str = cur.fetchone()

    if current_status == 'Vencido' and new_status == 'Pendiente':
        if venc_date_str:
            venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
            if venc_date <= datetime.now():
                print("La fecha de vencimiento debe ser en el futuro para cambiar el estado a Pendiente.")
                conn.close()
                return False

    cur.execute('UPDATE TAREAS SET status = ? WHERE id = ?', (new_status, tarea_id))
    conn.commit()
    conn.close()

    return cur.rowcount > 0
def list_tareas(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM TAREAS WHERE user_id = ? AND STATUS != ?', (user_id,'Archivado'))
    tareas_data = cur.fetchall()
    conn.close()
    return [Tarea(**t) for t in tareas_data]

def read_tarea(tarea_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM TAREAS WHERE id = ?', (tarea_id,))
    tarea_data = cur.fetchone()
    conn.close()
    if tarea_data:
        return Tarea(**tarea_data)
    return None

def delete_tarea(tarea_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM TAREAS WHERE id = ?', (tarea_id,))
    conn.commit()
    rows_affected = cur.rowcount
    conn.close()
    if rows_affected > 0:
        db_logger.info(f"Tarea removida: ID {tarea_id}")
    else:
        db_logger.warning(f"Intento de remover tarea no existente: ID {tarea_id}")
    return rows_affected > 0

def filtered_search_tareas(user_id, titulo=None, fecha_inicio=None, fecha_fin=None, etiqueta1=None, etiqueta2=None, status=None):
    conn = get_db_connection()
    cur = conn.cursor()

    query = 'SELECT * FROM TAREAS WHERE user_id = ?'
    params = [user_id]

    if titulo:
        query += ' AND titulo LIKE ?'
        params.append(f'%{titulo}%')

    if fecha_inicio:
        query += ' AND venc_date >= ?'
        params.append(fecha_inicio)

    if fecha_fin:
        query += ' AND venc_date <= ?'
        params.append(fecha_fin)

    if etiqueta1:
        query += ' AND etiqueta1 = ?'
        params.append(etiqueta1)

    if etiqueta2:
        query += ' AND etiqueta2 = ?'
        params.append(etiqueta2)

    if status:
        query += ' AND status = ?'
        params.append(status)

    cur.execute(query, params)
    tareas_data = cur.fetchall()
    conn.close()
    return [Tarea(**t) for t in tareas_data]