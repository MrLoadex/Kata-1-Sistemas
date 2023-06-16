import tkinter as tk
import student_database_impl
import front
import front_login


def login():
    app = front_login.AuthenticationWindow()
    app.mainloop()
    access = app.access # Obtener el valor de retorno de la función ejecutada en el objeto
    #AComprueba que haya obtenido acceso
    if access:
        open_window()


def open_window():
    #creo la coneccion con la base de datos
    student_database_impl.connect_db()

    # Crear la ventana principal
    window = front.Window()

    # Crear el frame de listado en la solapa de Listado
    listado_frame = front.ListedFrame(window.flap_list)
    listado_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el frame de agregar en la solapa de Agregar
    agregar_frame = front.AddFrame(window.flap_add)
    agregar_frame.pack(expand=True, padx=50, pady=10)

    # Crear el frame de buscar en la solapa de Buscar
    buscar_frame = front.BuscarFrame(window.flap_search)
    buscar_frame.pack(expand=True, padx=50, pady=10)

    # Ejemplo de agregar estudiantes al listado
    listado_frame.add_student()

    # Iniciar el bucle de eventos
    window.mainloop()
    
    
login()