# main.py

from database import init_db
from crudServices import create_user, get_user, verify_password, create_tarea, read_tarea, update_tarea, delete_tarea, list_tareas
from migrations import run_migrations
from getpass import getpass

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
        print("\n1. Crear tarea\n2. Listar tareas\n3. Actualizar tarea\n4. Eliminar tarea\n5. Salir")
        choice = input("Elija una opción: ")

        if choice == '1':
            titulo = input("Ingrese el título de la tarea: ")
            descripcion = input("Ingrese la descripción de la tarea: ")
            etiqueta = input("Ingrese la etiqueta de la tarea (opcional): ")
            venc_date = input("Ingrese la fecha de vencimiento (AAAA-MM-DD HH:MM:SS, opcional): ")
            create_tarea(titulo, descripcion, etiqueta, venc_date, user.id)
            print("Tarea creada exitosamente.")

        elif choice == '2':
            tareas = list_tareas(user.id)
            for tarea in tareas:
                print(f"{tarea.id}: {tarea.titulo} - {'Completada' if tarea.completado else 'Pendiente'}")

        elif choice == '3':
            tarea_id = int(input("Ingrese el ID de la tarea a actualizar: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                titulo = input(f"Ingrese el nuevo título ({tarea.titulo}): ") or tarea.titulo
                descripcion = input(f"Ingrese la nueva descripción ({tarea.descripcion}): ") or tarea.descripcion
                etiqueta = input(f"Ingrese la nueva etiqueta ({tarea.etiqueta}): ") or tarea.etiqueta
                venc_date = input(f"Ingrese la nueva fecha de vencimiento ({tarea.venc_date}): ") or tarea.venc_date
                status = input("Ingrese el estado (pendiente/en_progreso/completado/archivado): ")
                pendiente = status == 'pendiente'
                in_progress = status == 'en_progreso'
                completado = status == 'completado'
                archivado = status == 'archivado'
                update_tarea(tarea_id, titulo, descripcion, etiqueta, venc_date, pendiente, in_progress, completado, archivado)
                print("Tarea actualizada exitosamente.")
            else:
                print("Tarea no encontrada o no tiene permiso para actualizarla.")

        elif choice == '4':
            tarea_id = int(input("Ingrese el ID de la tarea a eliminar: "))
            tarea = read_tarea(tarea_id)
            if tarea and tarea.user_id == user.id:
                delete_tarea(tarea_id)
                print("Tarea eliminada exitosamente.")
            else:
                print("Tarea no encontrada o no tiene permiso para eliminarla.")

        elif choice == '5':
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()