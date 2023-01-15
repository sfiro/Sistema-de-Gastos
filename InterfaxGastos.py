import tkinter as tk
from tkinter import ttk
import mysql.connector




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

        # ----------- conexion a la base de datos ------------------------
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='3231213',
            db='INGENIO'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT database();")
        registro = self.cursor.fetchone()

        print("conexion establecida exitosamente")
        print("la base de datos se llama:",registro)

        self.title("Agregar Proveedor")
        self.geometry("1200x900")

        self.columnconfigure(0, weight=1, minsize=70)

        self.frame1 = tk.Frame(master=self)
        self.frame1.grid(row=0,column=0,sticky="nw")
        

        self.frame2 = tk.Frame(master=self)
        self.frame2.grid(row=0,column=1,sticky="nw")

        self.frame3 = tk.Frame(master=self)
        self.frame3.grid(row=1,column=0,columnspan=2)

# ------------------ label de la ventana proveedores -------------------------------------

        self.empresa = tk.Label(master = self.frame1, text = "Empresa:")
        self.empresa.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.representante = tk.Label(master = self.frame1, text = "Representante legal:")
        self.representante.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.nit = tk.Label(master = self.frame1, text = "NIT:")
        self.nit.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.celular = tk.Label(master = self.frame1, text = "Celular:")
        self.celular.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.pyme = tk.Label(master = self.frame1, text = "Es PYME:")
        self.pyme.grid(row = 4, column = 0, padx = 10, pady = 10)

        self.departamento = tk.Label(master = self.frame1, text = "Departamento:")
        self.departamento.grid(row = 5, column = 0, padx = 10, pady = 10)

        self.municipio = tk.Label(master = self.frame1, text = "Municipio:")
        self.municipio.grid(row = 6, column = 0, padx = 10, pady = 10)

        self.direccion= tk.Label(master = self.frame1, text = "Direccion:")
        self.direccion.grid(row = 7, column = 0, padx = 10, pady = 10)

        self.categoria = tk.Label(master = self.frame1, text = "Categoria:")
        self.categoria.grid(row = 8, column = 0, padx = 10, pady = 10)

        self.descripcion = tk.Label(master = self.frame1, text = "Descripcion:")
        self.descripcion.grid(row = 9, column = 0, padx = 10, pady = 10)

        self.rutButton = tk.Button(master=self.frame1,text="Adjuntar RUT",command=self.guardar)
        self.rutButton.grid(row=10,column=0,padx=10,pady=10)

# ------------------ Entry de la ventana proveedores -------------------------------------

        self.entradaEmpresa = tk.Entry(master = self.frame1, textvariable="Empresa:")
        self.entradaEmpresa.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.entradaRepresentante = tk.Entry(master = self.frame1, textvariable="Representante:")
        self.entradaRepresentante.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.entradaNIT = tk.Entry(master = self.frame1, textvariable="NIT:")
        self.entradaNIT.grid(row = 2, column = 1, padx = 10, pady = 10)

        self.entradaTelefono = tk.Entry(master = self.frame1, textvariable="Telefono:")
        self.entradaTelefono.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.comboBoxPyme = ttk.Combobox(master = self.frame1)
        self.comboBoxPyme['values'] = ("SI","NO")
        self.comboBoxPyme.grid(row = 4, column = 1, padx = 10, pady = 10)

        def seleccion(event): #evento que actuliza la base de datos del combobox municipio en base a la seleccion del departamento
    
            sql = "SELECT municipio FROM municipios WHERE departamento = '{}';".format(self.comboBoxDepartamento.get())  
            self.cursor.execute(sql)
            valores =[]
            for valor in self.cursor.fetchall():
                valores.append(valor[0])
            self.comboBoxMunicipio['values'] = valores

# -----combobox de departamentos, se hace la consulta a SQL y se traen todos los datos de la tabla
        self.comboBoxDepartamento = ttk.Combobox(master = self.frame1)
        sql = "SELECT nombre FROM Departamentos " 
        self.cursor.execute(sql)
        valores =[]
        for valor in self.cursor.fetchall():
            valores.append(valor[0])
        self.comboBoxDepartamento['values'] = valores
        self.comboBoxDepartamento.grid(row = 5, column = 1, columnspan=2, padx = 10, pady = 10)
        self.comboBoxDepartamento.bind("<<ComboboxSelected>>",seleccion) #este es un evento que ocurre al generar un cambo en el combobox departamento

# ---- El valor seleccionado en departamento debe filtrar las opciones del combobox de municipios
        self.comboBoxMunicipio = ttk.Combobox(master = self.frame1)
        self.comboBoxMunicipio.grid(row = 6, column = 1, padx = 10, pady = 10)

        self.entradaDireccion = tk.Entry(master = self.frame1, text = "Direccion:")
        self.entradaDireccion.grid(row = 7, column = 1, padx = 10, pady = 10)

        self.comboBoxCategoria = ttk.Combobox(master = self.frame1)
        self.comboBoxCategoria['values'] = ("Madera","Impresiones")
        self.comboBoxCategoria.grid(row = 8, column = 1, padx = 10, pady = 10)

        self.entradaDescripcion = tk.Entry(master = self.frame1, text = "descripcion:")
        self.entradaDescripcion.grid(row = 9, column = 1, padx = 10, pady = 10)

        self.labelRut = tk.Label(master = self.frame1, text = "Vacio")
        self.labelRut.grid(row = 10, column = 1, padx = 10, pady = 10)

#----------------- frame 2 proveedores -------------------------------------------

        self.guardarButton = tk.Button(master=self.frame2,text="Guardar",command=self.guardar)
        self.guardarButton.grid(row=0,column=0,padx=10,pady=10)

        self.actualizarButton = tk.Button(master=self.frame2,text="Actualizar",command=self.actualizar)
        self.actualizarButton.grid(row=0,column=1,padx=10,pady=10)

        self.eliminarButton = tk.Button(master=self.frame2,text="Eliminar",command=self.eliminar)
        self.eliminarButton.grid(row=0,column=2,padx=10,pady=10)

#-------------------frame 3 proveedores treeview ----------------------------------

        self.treeview = ttk.Treeview(master=self.frame3,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11'))
        
        self.scrollbarTree = ttk.Scrollbar(master=self.frame3,orient="horizontal")
        self.treeview.configure(xscrollcommand=self.scrollbarTree.set)
        self.scrollbarTree.config(command=self.treeview.xview)
        

        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=70)
        self.treeview.heading('col1', text='Empresa')
        self.treeview.heading('col2', text='Representante')
        self.treeview.heading('col3', text='NIT')
        self.treeview.heading('col4', text='Es PYME')
        self.treeview.heading('col5', text='Departamento')
        self.treeview.heading('col6', text='Municipio')
        self.treeview.heading('col7', text='Direccion')
        self.treeview.heading('col8', text='Categoria')
        self.treeview.heading('col9', text='Descripcion')
        self.treeview.heading('col10', text='RUT')
        self.treeview.heading('col11', text='Telefono')
        self.treeview.grid(row = 1, column = 0, columnspan = 3, sticky="nsew")
        self.scrollbarTree.grid(row = 2, column = 0, sticky="ew")

        self.refrescar()
    
    
    def guardar(self):
        empresa = self.entradaEmpresa.get()
        representante = self.entradaRepresentante.get()
        nit = self.entradaNIT.get()
        telefono = self.entradaTelefono.get()
        espyme = self.comboBoxPyme.get()
        departamento = self.comboBoxDepartamento.get()
        municipio = self.comboBoxMunicipio.get()
        direccion = self.entradaDireccion.get()
        categoria = self.comboBoxCategoria.get()
        descripcion = self.entradaDescripcion.get()


        self.cursor.execute("INSERT INTO proveedores(Empresa,Representante,Nit,EsPyme,Departamento,Municipio,Direccion,Categoria,Descripcion,Telefono) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(empresa,representante,nit,espyme,departamento,municipio,direccion,categoria,descripcion,telefono))
        self.connection.commit()
        self.refrescar()

    def eliminar(self):
        pass

    def actualizar(self):
        pass

    def refrescar(self):
        #self.entradaNombre.delete(0,tk.END)
        #self.entradaTelefono.delete(0,tk.END)
        #self.entradaCorreo.delete(0,tk.END)
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT * FROM Proveedores"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            #print(dato)
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
             #self.lista.insert(n,list(dato[:]))
            n = n+1
    def validar(self):
        #if self.entradaEmpresa.get() == "":
        # representante = self.entradaRepresentante.get()
        # nit = self.entradaNIT.get()
        # telefono = self.entradaTelefono.get()
        # espyme = self.comboBoxPyme.get()
        # departamento = self.comboBoxDepartamento.get()
        # municipio = self.comboBoxMunicipio.get()
        # direccion = self.entradaDireccion.get()
        # categoria = self.comboBoxCategoria.get()
        # descripcion = self.entradaDescripcion.get()


        



if __name__ == "__main__":
    VentanaGastos = SeguimientoGastos()
    VentanaGastos.mainloop()