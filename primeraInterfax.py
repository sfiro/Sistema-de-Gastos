import tkinter as tk
import mysql.connector

class interfax(tk.Tk):
    def __init__(self):
        super().__init__()

#----------- conexion a la base de datos ------------------------
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='3231213a',
            db='INGENIO'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT database();")
        registro = self.cursor.fetchone()

        print("conexion establecida exitosamente")
        print("la base de datos se llama:",registro)
        self.idVendedor = 0

        

# ------------- creación de la ventana grafica ------------------

        self.title("Vendedores")
        self.geometry("500x350")
        self.columnconfigure((0,1),weight=1)

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
        self.entradaNombre.grid(row = 0, column = 1, columnspan= 3, sticky="nsew")
        self.entradaTelefono = tk.Entry(master = self, textvariable="Telefono")
        self.entradaTelefono.grid(row = 1, column = 1, columnspan= 3, sticky="nsew")
        self.entradaCorreo = tk.Entry(master = self, textvariable="Correo")
        self.entradaCorreo.grid(row = 2, column = 1, columnspan= 3, sticky="nsew")
        

#----------------Botones de acción -----------------------------------------------------
        self.ingresarButton = tk.Button(master=self,text="INGRESAR",command=self.ingresar)
        self.ingresarButton.grid(row=3,column=0,padx=10,pady=10)
        self.actualizarButton = tk.Button(master=self,text="ACTUALIZAR",command=self.actualizar)
        self.actualizarButton.grid(row=3,column=1,padx=10,pady=10)
        self.eliminarButton = tk.Button(master=self,text="ELIMINAR",command=self.eliminar)
        self.eliminarButton.grid(row=3,column=2,padx=10,pady=10)
        self.cargarButton = tk.Button(master=self,text="CARGAR",command=self.cargar)
        self.cargarButton.grid(row=3,column=3,padx=10,pady=10)

#----------------List BOX  -----------------------------------------------------   
        self.lista = tk.Listbox(master=self)
        self.lista.grid(row = 4, column = 0, columnspan = 4, sticky="nsew")
        self.scrollbar = tk.Scrollbar(master=self,orient="vertical" ,command=self.lista.yview)
        self.lista.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row = 4, column = 3,sticky="nse")

        self.refrescar()

    def ingresar(self):
        #print("hola")
        name = self.entradaNombre.get()
        email = self.entradaCorreo.get()
        phone = self.entradaTelefono.get()
        self.cursor.execute("INSERT INTO Vendedores(vendedor,correo,telefono) VALUES('{}','{}','{}');".format(name,email,phone))
        self.connection.commit()
        print(name + email + phone)
        self.refrescar()

    def eliminar(self):
        sql = "DELETE FROM Vendedores WHERE idvendedor = {}".format(self.idVendedor)
        self.cursor.execute(sql)
        self.connection.commit()
        self.refrescar()
        
    
    def actualizar(self):
        print(self.idVendedor)
        name = self.entradaNombre.get()
        email = self.entradaCorreo.get()
        phone = self.entradaTelefono.get()
        #sql = "UPDATE FROM Vendedores(vendedor,correo,telefono) VALUES('{}','{}','{}');".format(name,email,phone)
        self.cursor.execute("UPDATE Vendedores SET vendedor = '{}',correo = '{}',telefono='{}' WHERE idvendedor = '{}'".format(name,email,phone,self.idVendedor))
        self.connection.commit()
        self.refrescar()


    def refrescar(self):
        self.entradaNombre.delete(0,tk.END)
        self.entradaTelefono.delete(0,tk.END)
        self.entradaCorreo.delete(0,tk.END)
        self.lista.delete(0,"end")
        sql = "SELECT * FROM Vendedores"
        self.cursor.execute(sql)
        n=0
        for dato in self.cursor.fetchall():
            self.lista.insert(n,list(dato[:]))
            n = n+1
        #self.connection.commit()
    def cargar(self):
        
        self.entradaNombre.delete(0,tk.END)
        self.entradaTelefono.delete(0,tk.END)
        self.entradaCorreo.delete(0,tk.END)

        indice = self.lista.curselection()[0]
        datos=self.lista.get(indice)
        self.idVendedor = datos[0]
        self.entradaNombre.insert(0,datos[1])
        self.entradaCorreo.insert(0,datos[2])
        self.entradaTelefono.insert(0,datos[3])

        
        

if __name__ == "__main__":
    ventana = interfax()
    ventana.mainloop()



