from database import init_db
from crudServices import create_user, get_user, verify_password, create_tarea, read_tarea, update_tarea, update_tarea_status, delete_tarea, list_tareas, filtered_search_tareas
from migrations import run_migrations
from getpass import getpass
from datetime import datetime
from loggerSetup import user_logger

def authenticate_user():
    while True:
        choice = input("1. Iniciar sesión\n2. Crear nuevo usuario\nElija una opción: ")
        if choice == '1':
            nombre = input("Ingrese su nombre de usuario: ")
            password = getpass("Ingrese su contraseña: ")
            user = get_user(nombre)
            if user and verify_password(password, user.password):
                user_logger.info(f"Usuario ha iniciado sesión: {nombre}")
                return user
            else:
                user_logger.warning(f"Intento de inicio de sesión fallido para el usuario: {nombre}")
                print("Nombre de usuario o contraseña inválidos.")
        elif choice == '2':
            nombre = input("Ingrese un nuevo nombre de usuario: ")
            password = getpass("Ingrese una nueva contraseña: ")
            user_id = create_user(nombre, password)
            if user_id is None:
                print("El nombre de usuario ya existe. Por favor, elija otro.")
            else:
                user_logger.info(f"Nueva cuenta de usuario creada: {nombre}")
                print("Usuario creado exitosamente.")
                return get_user(nombre)
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def select_etiqueta1():
    print("\nSeleccione etiqueta 1:")
    print("1. Personal")
    print("2. Academico")
    print("3. Trabajo")
    choice = input("Elija una opción (1-3): ")
    options = {
        '1': 'Personal',
        '2': 'Academico',
        '3': 'Trabajo'
    }
    return options.get(choice, None)

def select_etiqueta2():
    print("\nSeleccione etiqueta 2:")
    print("1. Prioridad alta")
    print("2. Prioridad media")
    print("3. Prioridad baja")
    choice = input("Elija una opción (1-3): ")
    options = {
        '1': 'Prioridad alta',
        '2': 'Prioridad media',
        '3': 'Prioridad baja'
    }
    return options.get(choice, None)

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Formato de fecha inválido. Utilice AAAA-MM-DD o deje en blanco.")

def main():
    init_db()
    run_migrations()

    user = authenticate_user()
    print(f"Bienvenido, {user.nombre}!")
    user_logger.info(f"Sesión de usuario iniciada: {user.nombre}")

    while True:
        print("\n1. Crear tarea\n2. Listar tareas\n3. Actualizar tarea\n4. Cambiar estado de tarea\n5. Eliminar tarea\n6. Búsqueda con filtros\n7. Salir")
        choice = input("Elija una opción: ")

        if choice == '1':
            titulo = input("Ingrese el título de la tarea: ")
            descripcion = input("Ingrese la descripción de la tarea: ")
            etiqueta1 = select_etiqueta1()
            etiqueta2 = select_etiqueta2()
            venc_date_str = input("Ingrese la fecha de vencimiento (AAAA-MM-DD HH:MM:SS, opcional): ")
            venc_date = None
            if venc_date_str:
                try:
                    venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Formato de fecha inválido. La tarea se creará sin fecha de vencimiento.")
            create_tarea(titulo, descripcion, etiqueta1, etiqueta2, venc_date, user.id)
            print("Tarea creada exitosamente.")
            user_logger.info(f"Usuario {user.nombre} ha creado una nueva tarea")

        elif choice == '2':
            tareas = list_tareas(user.id)
            for tarea in tareas:
                print(f"ID: {tarea.id}, Título: {tarea.titulo}, Estado: {tarea.status}, Descripcion: {tarea.descripcion}\n,  Etiqueta 1: {tarea.etiqueta1}, Etiqueta 2: {tarea.etiqueta2}, Vencimiento: {tarea.venc_date or 'No especificado'}\n")
                user_logger.info(f"Usuario {user.nombre} ha listado sus tareas")
        elif choice == '3':
            tarea_id = int(input("Ingrese el ID de la tarea a actualizar: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                titulo = input(f"Ingrese el nuevo título ({tarea.titulo}): ") or tarea.titulo
                descripcion = input(f"Ingrese la nueva descripción ({tarea.descripcion}): ") or tarea.descripcion
                etiqueta1 = select_etiqueta1() or tarea.etiqueta1
                etiqueta2 = select_etiqueta2() or tarea.etiqueta2
                venc_date_str = input(f"Ingrese la nueva fecha de vencimiento ({tarea.venc_date}, formato AAAA-MM-DD HH:MM:SS): ") or tarea.venc_date
                venc_date = None
                if venc_date_str:
                    try:
                        venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        print("Formato de fecha inválido. Se mantendrá la fecha de vencimiento anterior.")
                        venc_date = datetime.strptime(tarea.venc_date, "%Y-%m-%d %H:%M:%S") if tarea.venc_date else None
                update_tarea(tarea_id, titulo, descripcion, etiqueta1, etiqueta2, venc_date)
                print("Tarea actualizada exitosamente.")
                user_logger.info(f"Usuario {user.nombre} ha actualizado una tarea")
            else:
                print("Tarea no encontrada o no tiene permiso para actualizarla.")
            

        elif choice == '4':
            tarea_id = int(input("Ingrese el ID de la tarea para cambiar su estado: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                print(f"Estado actual: {tarea.status}")
                if tarea.status == 'Pendiente':
                    new_status = 'En progreso'
                elif tarea.status == 'En progreso':
                    new_status = 'Completado'
                elif tarea.status == 'Completado':
                    new_status = 'Archivado'
                elif tarea.status == 'Vencido':
                    print("Para actualizar una tarea vencida, se requiere actualizar la fecha de vencimiento.")
                    venc_date_str = input("Ingrese la nueva fecha de vencimiento (AAAA-MM-DD HH:MM:SS): ")
                    try:
                        venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
                        if venc_date > datetime.now():
                            new_status = 'Pendiente'
                            update_tarea(tarea_id, tarea.titulo, tarea.descripcion, tarea.etiqueta1, tarea.etiqueta2, venc_date)
                            print(f"Fecha de vencimiento actualizada. Estado cambiado a {new_status}.")
                        else:
                            print("La fecha ingresada está en el pasado. La tarea permanece vencida.")
                            continue
                    except ValueError:
                        print("Formato de fecha inválido. No se puede actualizar el estado.")
                        continue
                else:
                    print("No se puede cambiar el estado de una tarea archivada.")
                    continue
                
                if update_tarea_status(tarea_id, new_status):
                    print(f"Estado de la tarea actualizado a: {new_status}")
                    user_logger.info(f"Usuario {user.nombre} ha cambiado el estado de una tarea")
                else:
                    print("No se pudo actualizar el estado de la tarea.")
            else:
                print("Tarea no encontrada o no tiene permiso para actualizarla.")
            
        elif choice == '5':
            tarea_id = int(input("Ingrese el ID de la tarea a eliminar: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                delete_tarea(tarea_id)
                print("Tarea eliminada exitosamente.")
                user_logger.info(f"Usuario {user.nombre} ha eliminado una tarea")
            else:
                print("Tarea no encontrada o no tiene permiso para eliminarla.")

        elif choice == '6':
            titulo = input("Ingrese el título a buscar (o deje en blanco): ")
            fecha_inicio = get_date_input("Ingrese la fecha de inicio (AAAA-MM-DD) o deje en blanco: ")
            fecha_fin = get_date_input("Ingrese la fecha de fin (AAAA-MM-DD) o deje en blanco: ")
            etiqueta1 = select_etiqueta1()
            etiqueta2 = select_etiqueta2()
            status = input("Ingrese el estado a buscar (Pendiente, En progreso, Completado, Archivado, Vencido) o deje en blanco: ")

            tareas = filtered_search_tareas(user.id, titulo, fecha_inicio, fecha_fin, etiqueta1, etiqueta2, status)
            
            if tareas:
                print("\nResultados de la búsqueda:")
                for tarea in tareas:
                    print(f"ID: {tarea.id}, Título: {tarea.titulo}, Estado: {tarea.status}, Etiqueta 1: {tarea.etiqueta1}, Etiqueta 2: {tarea.etiqueta2}, Vencimiento: {tarea.venc_date or 'No especificado'}")
            else:
                print("No se encontraron tareas que coincidan con los criterios de búsqueda.")
            user_logger.info(f"Usuario {user.nombre} ha realizado una búsqueda filtrada")

        elif choice == '7':
            print("¡Hasta luego!")
            user_logger.info(f"Sesión de usuario finalizada: {user.nombre}")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()