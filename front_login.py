import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from user_database_impl import get_user

class AuthenticationWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.access = False
        self.title("Autenticación")
        
        # Crear etiqueta y entrada para el usuario
        self.label_user = ttk.Label(self, text="Usuario:")
        self.label_user.pack()
        self.geometry("200x150")  # Tamaño fijo para la ventana
        self.resizable(False, False) #No redimencionable
        
        self.entry_user = ttk.Entry(self)
        self.entry_user.pack()
        
        # Crear etiqueta y entrada para la contraseña
        self.label_password = ttk.Label(self, text="Contraseña:")
        self.label_password.pack()
        
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack()
        
        # Crear botón de acceso
        self.button_login = ttk.Button(self, text="Acceder", command=self.login)
        self.button_login.pack(pady=10)
        
    def login(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        # Verificar las credenciales

        if get_user(username,password) != 0:
            messagebox.showinfo("Autenticación", "Acceso concedido")
            self.access = True
            self.destroy()
            return 1
        else:
            messagebox.showerror("Autenticación", "Credenciales incorrectas")
            self.entry_user.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            return 0

