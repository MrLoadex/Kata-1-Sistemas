import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import student_database_impl

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estudiantes")
        self.geometry("400x300")  # Tamaño fijo para la ventana
        self.resizable(False, False) #No redimencionable
        
        # Crear el controlador de las solapas
        self.flap_controller = ttk.Notebook(self)

        # Solapa de Listado
        self.flap_list = ttk.Frame(self.flap_controller)
        self.flap_controller.add(self.flap_list, text="Listado")

        # Solapa de Agregar
        self.flap_add = ttk.Frame(self.flap_controller)
        self.flap_controller.add(self.flap_add, text="Agregar")

        # Solapa de Buscar
        self.flap_search = ttk.Frame(self.flap_controller)
        self.flap_controller.add(self.flap_search, text="Buscar")

        # Posicionar el controlador de las solapas en la ventana utilizando grid
        self.flap_controller.grid(row=0, column=0, sticky="nsew")

        # Ajustar el tamaño de las filas y columnas para que se expandan con la ventana
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class ListadoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear un listado de textos con formato
        self.text_list = []

        # Crear un scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar el listbox con el scrollbar
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set, height=10,)
        self.listbox.grid(row=0, column=0, sticky="nsew")


        # Vincular el scrollbar con el listbox
        self.scrollbar.config(command=self.listbox.yview)

        # Crear un frame para el botón de actualización
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Crear el botón de actualización
        self.button_update = ttk.Button(self.button_frame, text="Actualizar", command=self.add_student)
        self.button_update.pack()

        # Configurar el tamaño fijo del listado de nombres
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #Actualiza la lista de estudiantes
        self.add_student()
        
    def add_student(self):
        self.listbox.delete(0, tk.END)
        student_list = student_database_impl.show_students()
        # Recorro la lista de estudiantes y voy imprimiéndolos
        for student in student_list:
            student_id = student[0]
            name = student[1]
            DNI = student[2]
            career = student[3]
            
            self.listbox.insert(tk.END, "ID: {}".format(student_id))
            self.listbox.insert(tk.END, "Nombre: {}".format(name))
            self.listbox.insert(tk.END, "DNI: {}".format(DNI))
            self.listbox.insert(tk.END, "Carrera: {}".format(career))
            self.listbox.insert(tk.END, "")  # Línea vacía como separador


class AgregarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Crear los labels y los Entry
        self.label_apellido_nombre = ttk.Label(self, text="Apellido y Nombre:")
        self.entry_apellido_nombre = ttk.Entry(self)

        self.label_dni = ttk.Label(self, text="DNI:")
        self.entry_dni = ttk.Entry(self)

        self.label_carrera = ttk.Label(self, text="Carrera:")
        self.entry_carrera = ttk.Entry(self)

        # Crear el botón de agregar
        self.button_agregar = ttk.Button(self, text="Agregar", command=self.agregar_estudiante, state=tk.DISABLED)

        # Crear el label de éxito
        self.label_exito = ttk.Label(self, text="", foreground="green")

        # Posicionar los elementos utilizando grid
        self.label_apellido_nombre.grid(row=0, column=0, sticky="w")
        self.entry_apellido_nombre.grid(row=1, column=0)

        self.label_dni.grid(row=2, column=0, sticky="w")
        self.entry_dni.grid(row=3, column=0)

        self.label_carrera.grid(row=4, column=0, sticky="w")
        self.entry_carrera.grid(row=5, column=0)

        self.button_agregar.grid(row=6, column=0)

        self.label_exito.grid(row=7, column=0)
        
        # Vincular la validación de los Entry a la actualización del estado del botón
        self.entry_apellido_nombre.bind("<KeyRelease>", self.actualizar_estado_boton)
        self.entry_dni.bind("<KeyRelease>", self.actualizar_estado_boton)
        self.entry_carrera.bind("<KeyRelease>", self.actualizar_estado_boton)
        
    def actualizar_estado_boton(self, event=None):
        # Obtener los valores de los Entry
        apellido_nombre = self.entry_apellido_nombre.get()
        dni = self.entry_dni.get()
        carrera = self.entry_carrera.get()

        # Verificar si los Entry están completos
        if apellido_nombre and dni and carrera:
            self.button_agregar.config(state=tk.NORMAL)  # Habilitar el botón
        else:
            self.button_agregar.config(state=tk.DISABLED) #deshabilitarlo
            
    def agregar_estudiante(self):
        #recupero los datos
        name = self.entry_apellido_nombre.get()
        DNI = self.entry_dni.get()
        career =  self.entry_carrera.get()
        
        #los inserto en la base de datos
        student_database_impl.add_student(name,DNI,career)
        
        self.label_exito.config(text="Agregado con éxito")
        # Ocultar el label de éxito después de 2 segundos
        self.after(1000, self.ocultar_label_exito)
        
    def ocultar_label_exito(self):
        self.label_exito.config(text="")


class BuscarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear el label de ID y el entry
        self.label_id = ttk.Label(self, text="ID:")
        self.entry_id = ttk.Entry(self)

        # Crear el botón de buscar
        self.button_buscar = ttk.Button(self, text="Buscar", command=self.buscar_estudiante)

        # Crear la línea horizontal
        self.line = ttk.Separator(self, orient=tk.HORIZONTAL)

        # Crear el label de información
        self.label_info = ttk.Label(self, text="id: -\nnombre: -\ndni: -\ncarrera: -")

        # Crear el cartel "MODIFICAR"
        self.button_modificar = ttk.Button(self, text="MODIFICAR", command= self.modificar_estudiante, state=tk.DISABLED)


        # Crear el label de eliminar
        self.label_eliminar = ttk.Label(self, text="Eliminar", foreground="blue", cursor="hand2")
        self.label_eliminar.bind("<Button-1>", self.eliminar_estudiante)

        # Posicionar los elementos utilizando grid
        self.label_id.grid(row=0, column=0, sticky="w")
        self.entry_id.grid(row=0, column=1)
        self.button_buscar.grid(row=0, column=2, padx=(10, 0))
        self.line.grid(row=1, column=0, columnspan=3, sticky="we", pady=10)
        self.label_info.grid(row=2, column=0, columnspan=3, pady=10)
        self.button_modificar.grid(row=3, column=0, columnspan=3, pady=10)
        self.label_eliminar.grid(row=4, column=0, columnspan=3, pady=10)

    def buscar_estudiante(self):
        id = self.entry_id.get()
        student = student_database_impl.get_student(id)
        if student != 0:    
            name = student[0]
            DNI = student[1]
            career = student[2]
            self.label_info.config(text="id: " + str(id) + "\nnombre: " + name + "\ndni: " + str(DNI) + "\ncarrera: " + career)
            self.button_modificar.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Estudiante no encontrado")

        

    def modificar_estudiante(self):
        id = self.entry_id.get()
        ventana_modificar = VentanaModificar(id)
        ventana_modificar.mainloop()
        
    def eliminar_estudiante(self, event):
        id = self.entry_id.get()
        respuesta = messagebox.askyesno("Advertencia", "Esta accion sera permanente y no podra deshacerse")
        if respuesta:
            student_database_impl.del_student(id)
            messagebox.showinfo("Éxito", "El estudiante se eliminó con éxito")

class VentanaModificar(tk.Toplevel):
    def __init__(self,id):
        super().__init__()
        self.title("Modificar")
        self.geometry("400x200")
        self.id = id
        # Crear los labels y los Entry
        self.label_apellido_nombre = tk.Label(self, text="Apellido y Nombre:")
        self.entry_apellido_nombre = tk.Entry(self)

        self.label_dni = tk.Label(self, text="DNI:")
        self.entry_dni = tk.Entry(self)

        self.label_carrera = tk.Label(self, text="Carrera:")
        self.entry_carrera = tk.Entry(self)

        # Posicionar los elementos utilizando grid
        self.label_apellido_nombre.grid(row=0, column=0, sticky="w")
        self.entry_apellido_nombre.grid(row=1, column=0, padx=10)

        self.label_dni.grid(row=2, column=0, sticky="w")
        self.entry_dni.grid(row=3, column=0, padx=10)

        self.label_carrera.grid(row=4, column=0, sticky="w")
        self.entry_carrera.grid(row=5, column=0, padx=10)

        # Crear el frame para los botones
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=6, column=0, pady=10)

        # Crear el botón Modificar
        self.button_modificar = tk.Button(self.button_frame, text="Modificar", command=self.modificar_estudiante)
        self.button_modificar.grid(row=0, column=0, padx=5)

        # Crear el botón Cancelar
        self.button_cancelar = tk.Button(self.button_frame, text="Cancelar", command=self.destroy)
        self.button_cancelar.grid(row=0, column=1, padx=5)

    def modificar_estudiante(self):
        
        #recoje los datos
        apellido_nombre = self.entry_apellido_nombre.get()
        dni = self.entry_dni.get()
        carrera = self.entry_carrera.get()
        print(apellido_nombre,dni,carrera)
        #modifica la base de datos
        student_database_impl.update_student(DNI=dni, name= apellido_nombre, career= carrera, student_id= self.id)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Estudiante modificado con éxito.")

        # Cerrar la ventana de modificar
        self.destroy()


#creo la coneccion con la base de datos
student_database_impl.connect_db()

# Crear la ventana principal
window = Window()

# Crear el frame de listado en la solapa de Listado
listado_frame = ListadoFrame(window.flap_list)
listado_frame.pack(fill=tk.BOTH, expand=True)

# Crear el frame de agregar en la solapa de Agregar
agregar_frame = AgregarFrame(window.flap_add)
agregar_frame.pack(expand=True, padx=50, pady=10)

# Crear el frame de buscar en la solapa de Buscar
buscar_frame = BuscarFrame(window.flap_search)
buscar_frame.pack(expand=True, padx=50, pady=10)

# Ejemplo de agregar estudiantes al listado
listado_frame.add_student()

# Iniciar el bucle de eventos
window.mainloop()