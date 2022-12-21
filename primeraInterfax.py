import tkinter as tk


class interfax(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Vendedores")
        self.geometry("400x300")
        self.columnconfigure((0,1,2),weight=1)

        self.rowconfigure((0,1,2,3,4),weight=0)

# ------------- Etiquetas-------------------------------------------------------
        self.nombre = tk.Label(master = self, text = "Nombre :")
        self.nombre.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.telefono = tk.Label(master = self, text = "Telefono :")
        self.telefono.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.correo = tk.Label(master = self, text = "Correo :")
        self.correo.grid(row = 2, column = 0, padx = 10, pady = 10)
#----------------Data Entry -----------------------------------------------------
        self.entradaNombre = tk.Entry(master = self, textvariable="Nombre:")
        self.entradaNombre.grid(row = 0, column = 1, columnspan= 2, sticky="nsew")
        self.entradaTelefono = tk.Entry(master = self, textvariable="Telefono")
        self.entradaTelefono.grid(row = 1, column = 1, columnspan= 2, sticky="nsew")
        self.entradaCorreo = tk.Entry(master = self, textvariable="Correo")
        self.entradaCorreo.grid(row = 2, column = 1, columnspan= 2, sticky="nsew")

#----------------Botones de acción -----------------------------------------------------
        self.ingresarButton = tk.Button(master=self,text="INGRESAR",command=self.ingresar)
        self.ingresarButton.grid(row=3,column=0,padx=10,pady=10)
        self.actualizarButton = tk.Button(master=self,text="ACTUALIZAR",command=self.actualizar)
        self.actualizarButton.grid(row=3,column=1,padx=10,pady=10)
        self.eliminarButton = tk.Button(master=self,text="ELIMINAR",command=self.eliminar)
        self.eliminarButton.grid(row=3,column=2,padx=10,pady=10)

#----------------List BOX  -----------------------------------------------------   
        self.listaList = tk.Listbox(master=self)
        self.listaList.grid(row = 4, column = 0, columnspan = 3, sticky="nsew")

    def ingresar():
        pass
    def actualizar():
        pass
    def eliminar():
        pass

if __name__ == "__main__":
    ventana = interfax()
    ventana.mainloop()



