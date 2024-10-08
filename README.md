# Task 1: Aplicación para gestionar tareas.

> ### Nombres: 
- Carlos Vega Muñoz. (Desarrollador)
- Diego Veas Bastías. (QA)


> ### Descripción:

 Se nos ha solicitado una aplicación dedicada a la gestión de tareas. 
 - El programa deberá ser capaz de implementar el método CRUD para las tareas (crear, leer, actualizar y borrar).
 - Cada tarea debe tener un título, una descripción, una fecha de vencimiento, y una etiqueta que facilite la organización. Se implementará un sistema de búsqueda que pueda filtrar en base a cualquiera de los atributos de las tareas.
 - Se podrá gestionar el estado de las tareas avanzando en las categorias en el siguiente orden: "pendiente", "en progreso", "completado" y finalmente "archivado"
 - Se implementará un sistema de autenticación mediante un nombre de usuario y contraseña. La contraseña estará cifrada utilizando Hashing.
   
Para más información con respecto a los requerimientos de este trabajo, acceder al [Documento adjunto.](Tarea1-Requerimientos.docx)

Este repositorio tambien contiene un documento Excel con los [Ciclos de Pruebas](Registro-Pruebas-T1-INF331.xlsx) realizados en este trabajo.

El flujo de administración del código fuente se realizó mediante la entrategia de Git: __Ship/Show/Ask.__ Elegimos este paradigma porque nos permitía hacer que el desarrollo fuera más rápido y autónomo en la fusión de branches, lo que nos benefició en los ciclos de pruebas. Carlos fue el encargado de la realización del código, el cual fue subiendo en el repositorio inicialmente de forma directa en la rama principal. A medida que se fue avanzando en el desarrollo, se empezó a utilizar una rama alterna. Al momento de hacer las fusiones, Carlos realizaba pull requests las cuales Diego autorizaba (rol de revisor/aprobador), una vez fusionados los cambios se realizaron ciclos de pruebas que nos ofrecian un feedback para conversar sobre el código, esto nos facilitó el proceso para indicar aspectos que necesitaban modificación sin alterar el flujo de trabajo en general. 
    
> ### Instalación:
  
Se debe tener instalado __Python 3__, __Sqlite__ (o sqlite3) y __Bcrypt__ (de ser necesario descargarlo aparte). Con estos requisitos previos listos, solo se debe __clonar el repositorio__ en la carpeta deseada a través de la terminal. 

- Sqlite es una librería que implementa un motor de base de datos SQL independiente, pequeño y rápido.
- Bcrypt es una librería que nos permite codificar nuestras contraseñas utilizando Hashing.

En __Windows__:

- Python: Se puede descargar desde la [Página Oficial de Python](https://www.python.org/downloads/) seleccionando la versión deseada. (nosotros usamos Python 3.12.0)
- Sqlite: Se debe descargar desde la [Página Oficial de Sqlite](https://www.sqlite.org/download.html) y agregar la variable de entorno al PATH del computador.
- Bcrypt: Puede ser descargada por linea de comandos usando `pip install bcrypt`
  
En __Linux__:

- Python: Escribir por consola `Sudo apt-get install python3` (nosotros usamos Python 3.9.7)
- Sqlite: Escribir por consola `Pip install sqlite3`

> ### Cómo usar:

Con el repositorio clonado, se debe abrir la terminal (prompt, shell, cmd, símbolo de sistema, etc), acceder a la carpeta en la que se ubica el archivo y escribir por consola `python main.py` o `python3 main.py` para ejecutar el código principal. Si busca acceder a la base de datos creada, puede escribir por consola `sqlite3 inf331` ("inf331" corresponde al nombre de la base de datos asignado en el archivo `config.py`)

Como información adicional, el manejo de fechas utilizados en este trabajo utilizan el formato TimeStamp, por lo que deberán ser ingresados con el formato `AAAA-MM-DD XX:YY:ZZ` para que el programa lo reconozca como una fecha válida.

En la codificación se cuenta con `Logs` de las operaciones, estos registros se pueden encontrar en una carpeta llamada "logs" que se crea tras ejecutar la aplicación.

> ### Cómo contribuir:

Si desea contribuir en este código, puede contactarse con nosotros a través de los correos: `diego.veas@usm.cl`o `carlos.vegamu@usm.cl`

> ### Licencia:

Este proyecto cuenta con [Licencia](LICENSE.txt) conforme a los términos de la licencia MIT. 
