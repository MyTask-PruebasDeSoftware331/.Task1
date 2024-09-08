from database import init_db
from crudServices import create_user, get_user, verify_password, create_tarea, read_tarea, update_tarea, update_tarea_status, delete_tarea, list_tareas
from migrations import run_migrations
from getpass import getpass
from datetime import datetime

def authenticate_user():
    while True:
        choice = input("1. Iniciar sesión\n2. Crear nuevo usuario\nElija una opción: ")
        if choice == '1':
            nombre = input("Ingrese su nombre de usuario: ")
            password = getpass("Ingrese su contraseña: ")
            user = get_user(nombre)
            if user and verify_password(password, user.password):
                return user
            else:
                print("Nombre de usuario o contraseña inválidos.")
        elif choice == '2':
            nombre = input("Ingrese un nuevo nombre de usuario: ")
            password = getpass("Ingrese una nueva contraseña: ")
            user_id = create_user(nombre, password)
            return get_user(nombre)
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def main():
    init_db()
    run_migrations()

    user = authenticate_user()
    print(f"Bienvenido, {user.nombre}!")

    while True:
        print("\n1. Crear tarea\n2. Listar tareas\n3. Actualizar tarea\n4. Cambiar estado de tarea\n5. Eliminar tarea\n6. Salir")
        choice = input("Elija una opción: ")

        if choice == '1':
            titulo = input("Ingrese el título de la tarea: ")
            descripcion = input("Ingrese la descripción de la tarea: ")
            etiqueta = input("Ingrese la etiqueta de la tarea (opcional): ")
            venc_date_str = input("Ingrese la fecha de vencimiento (AAAA-MM-DD HH:MM:SS, opcional): ")
            venc_date = None
            if venc_date_str:
                try:
                    venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Formato de fecha inválido. La tarea se creará sin fecha de vencimiento.")
            create_tarea(titulo, descripcion, etiqueta, venc_date, user.id)
            print("Tarea creada exitosamente.")

        elif choice == '2':
            tareas = list_tareas(user.id)
            for tarea in tareas:
                print(f"{tarea.id}: {tarea.titulo} - Estado: {tarea.status}")

        elif choice == '3':
            tarea_id = int(input("Ingrese el ID de la tarea a actualizar: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                titulo = input(f"Ingrese el nuevo título ({tarea.titulo}): ") or tarea.titulo
                descripcion = input(f"Ingrese la nueva descripción ({tarea.descripcion}): ") or tarea.descripcion
                etiqueta = input(f"Ingrese la nueva etiqueta ({tarea.etiqueta}): ") or tarea.etiqueta
                venc_date_str = input(f"Ingrese la nueva fecha de vencimiento ({tarea.venc_date}, formato AAAA-MM-DD HH:MM:SS): ") or tarea.venc_date
                venc_date = None
                if venc_date_str:
                    try:
                        venc_date = datetime.strptime(venc_date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        print("Formato de fecha inválido. Se mantendrá la fecha de vencimiento anterior.")
                        venc_date = datetime.strptime(tarea.venc_date, "%Y-%m-%d %H:%M:%S") if tarea.venc_date else None
                update_tarea(tarea_id, titulo, descripcion, etiqueta, venc_date)
                print("Tarea actualizada exitosamente.")
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
                            update_tarea(tarea_id, tarea.titulo, tarea.descripcion, tarea.etiqueta, venc_date)
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
            else:
                print("Tarea no encontrada o no tiene permiso para eliminarla.")

        elif choice == '6':
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()