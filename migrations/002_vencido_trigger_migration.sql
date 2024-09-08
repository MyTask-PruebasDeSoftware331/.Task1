-- Drop the existing table
DROP TABLE IF EXISTS TAREAS;

-- Recreate the TAREAS table with the new status constraint and default value
CREATE TABLE TAREAS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    etiqueta VARCHAR(100) NULL,
    venc_date TIMESTAMP NULL,
    status VARCHAR(100) NOT NULL CHECK (status IN ('Pendiente', 'En progreso', 'Completado', 'Archivado', 'Vencido')) DEFAULT 'Pendiente',
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES USER(id)
);

-- Create trigger for INSERT operations
CREATE TRIGGER check_vencido_status_insert
AFTER INSERT ON TAREAS
FOR EACH ROW
WHEN NEW.venc_date IS NOT NULL AND NEW.venc_date < CURRENT_TIMESTAMP
     AND NEW.status NOT IN ('Completado', 'Archivado')
BEGIN
    UPDATE TAREAS SET status = 'Vencido' WHERE id = NEW.id;
END;

-- Create trigger for UPDATE operations
CREATE TRIGGER check_vencido_status_update
AFTER UPDATE ON TAREAS
FOR EACH ROW
WHEN NEW.venc_date IS NOT NULL AND NEW.venc_date < CURRENT_TIMESTAMP
     AND NEW.status NOT IN ('Completado', 'Archivado')
BEGIN
    UPDATE TAREAS SET status = 'Vencido' WHERE id = NEW.id;
END;