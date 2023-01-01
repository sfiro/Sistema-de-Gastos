import tkinter as tk
from tkinter import ttk
import mysql.connector



# -------------------- Ventana secundaria del modulo de gasto (agregar gasto)---------------------------------------
class AgregarGastos(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Agregar Gasto")
        self.geometry("500x300")

        self.ingresarButton = tk.Button(master=self,text="Guardar",command=self.guardar)
        self.ingresarButton.grid(row=0,column=0,padx=10,pady=10)
        self.actualizarButton = tk.Button(master=self,text="Eliminar",command=self.eliminar)
        self.actualizarButton.grid(row=0,column=1,padx=10,pady=10)
    
    def guardar(self):
        pass

    def eliminar(self):
        pass

# -------------------- Ventana secundaria del modulo de gasto (agregar proveedor)---------------------------------------
class AgregarProveedor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Agregar Proveedor")
        self.geometry("500x300")

        self.guardarButton = tk.Button(master=self,text="Guardar",command=self.guardar)
        self.guardarButton.grid(row=0,column=0,padx=10,pady=10)

        self.actualizarButton = tk.Button(master=self,text="Actualizar",command=self.actualizar)
        self.actualizarButton.grid(row=0,column=1,padx=10,pady=10)
        self.eliminarButton = tk.Button(master=self,text="Eliminar",command=self.eliminar)
        self.eliminarButton.grid(row=0,column=2,padx=10,pady=10)
    
    def guardar(self):
        pass

    def eliminar(self):
        pass

    def actualizar(self):
        pass

# -------------------- Ventana Principal del modulo de gasto ---------------------------------------
class SeguimientoGastos(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Seguimiento Gastos")
        self.geometry("500x300")

        self.ingresarButton = tk.Button(master=self,text="Agregar Gasto",command=self.gastos)
        self.ingresarButton.grid(row=0,column=0,padx=10,pady=10)
        self.actualizarButton = tk.Button(master=self,text="Agregar Proveedor",command=self.proveedor)
        self.actualizarButton.grid(row=1,column=0,padx=10,pady=10)
    
    def gastos(self):
        agregar = AgregarGastos()
        agregar.mainloop()

    def proveedor(self):
        proveedorIngreso = AgregarProveedor()
        proveedorIngreso.mainloop()


if __name__ == "__main__":
    VentanaGastos = SeguimientoGastos()
    VentanaGastos.mainloop()