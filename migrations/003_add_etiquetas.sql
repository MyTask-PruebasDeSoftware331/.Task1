ALTER TABLE TAREAS ADD COLUMN etiqueta1 VARCHAR(20) CHECK (etiqueta1 IN ('Personal', 'Academico', 'Trabajo'));
ALTER TABLE TAREAS ADD COLUMN etiqueta2 VARCHAR(20) CHECK (etiqueta2 IN ('Prioridad alta', 'Prioridad media', 'Prioridad baja'));

ALTER TABLE TAREAS DROP COLUMN etiqueta;