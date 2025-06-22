Papelería – Setup Rápido

Requisitos (Windows)

- Python 3.7+
  Descargar e instalar desde python.org.

- DB Browser for SQLite
  Instalar desde sqlitebrowser.org/download.

- Tkinter
  Viene con Python en Windows. Verificar:
  python -c "import tkinter; print('Tkinter OK')"
  Si da error, reinstalar Python incluyendo “tcl/tk and IDLE”.

- ttkbootstrap
Comando para instalar:
pip install ttkbootstrap

Preparar la Base de Datos

1. Abrir DB Browser for SQLite.
2. Click en New Database, guardar como papeleria.db en la carpeta del proyecto.
3. Ir a Execute SQL, cargar schema.sql y pulsar ▶ (el botoncito para correr la app xd)
5. En Browse Data, confirmar que existe el usuario:
   admin / admin

Yo recomiendo darle al botón "abrir una base de datos" y desde ahi seleccionar el  papeleria.db (en teoria ya corre la db ahi).

Ejecutar la Aplicación

Desde la carpeta del proyecto:
    python login.py
- Usuario: admin
- Contraseña: admin
