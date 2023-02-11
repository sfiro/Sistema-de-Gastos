import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog     #importante para tener ventanas de busqueda de archivos
import mysql.connector
import shutil   #necesario para copiar archivos
import os     #necesario para crear carpetas






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
        self.treeviewButton = tk.Button(master=self,text="TREEVIEW",command=self.tree)
        self.treeviewButton.grid(row=2,column=0,padx=10,pady=10)
    
    def gastos(self):
        agregar = AgregarGastos()
        agregar.mainloop()

    def proveedor(self):
        proveedorIngreso = AgregarProveedor()
        proveedorIngreso.mainloop()
    
    def tree(self):
        treeView = treeViewDashboard()
        treeView.mainloop()


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
        self.geometry("1600x900")

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

        self.rutButton = tk.Button(master=self.frame1,text="Adjuntar RUT",command=self.adjuntarRUT)
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

        self.seleccionarButton = tk.Button(master=self.frame2,text="Seleccionar",command=self.seleccionar)
        self.seleccionarButton.grid(row=0,column=0,padx=10,pady=10)

        self.guardarButton = tk.Button(master=self.frame2,text="Guardar",command=self.guardar)
        self.guardarButton.grid(row=0,column=1,padx=10,pady=10)

        self.actualizarButton = tk.Button(master=self.frame2,text="Actualizar",command=self.actualizar)
        self.actualizarButton.grid(row=0,column=2,padx=10,pady=10)

        self.eliminarButton = tk.Button(master=self.frame2,text="Eliminar",command=self.eliminar)
        self.eliminarButton.grid(row=0,column=3,padx=10,pady=10)

#-------------------frame 3 proveedores treeview ----------------------------------

        self.treeview = ttk.Treeview(master=self.frame3,columns=('col1','col2','col3','col4','col5','col6','col7'))
        self.scrollbarTree = ttk.Scrollbar(master=self.frame3,orient="horizontal")
        self.treeview.configure(xscrollcommand=self.scrollbarTree.set)
        self.scrollbarTree.config(command=self.treeview.xview)
        
        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=50)  #id
        self.treeview.column('#1', width=150) #empresa
        self.treeview.column('#2', width=150) #representante
        self.treeview.column('#3', width=100) #telefono
        self.treeview.column('#4', width=130) #departamento
        self.treeview.column('#5', width=130) #municipio
        self.treeview.column('#6', width=100) #categoria
        self.treeview.column('#7', width=130) #RUT


        self.treeview.heading('col1', text='Empresa')
        self.treeview.heading('col2', text='Representante')
        self.treeview.heading('col3', text='Telefono')
        self.treeview.heading('col4', text='Departamento')
        self.treeview.heading('col5', text='Municipio')
        self.treeview.heading('col6', text='Categoria')
        self.treeview.heading('col7', text='RUT')
        self.treeview.grid(row = 0, column = 0, sticky="nsew")
        self.scrollbarTree.grid(row = 1, column = 0, sticky="nsew")

        self.SeleccionRegistro = False #validador de la selección de un registro
        self.idItem = 0

        self.refrescar()
    
    
    def guardar(self):
        valor = self.validar()
        
        if valor & ~self.SeleccionRegistro: #verifica si todos los campos se encuentran llenos y que no se halla seleccionado algún registro ya ingresado
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

            if self.archivo != "":
                destino = "/Users/debbiearredondo/desktop/prueba"     #se debe guardar la ruta del destino de los RUT  <<<<<<< SE DEBE CAMBIAR !!!
                nombreRUT = os.path.basename(self.archivo) #guarda el nombre del archivo
                os.makedirs(destino, mode=0o777, exist_ok=True)
                shutil.copy(self.archivo, destino)        #hace una copia del archivo

            self.cursor.execute("INSERT INTO proveedores(Empresa,Representante,Nit,EsPyme,Departamento,Municipio,Direccion,Categoria,Descripcion,Telefono,Archivo) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(empresa,representante,nit,espyme,departamento,municipio,direccion,categoria,descripcion,telefono,nombreRUT))
            self.connection.commit()
            self.refrescar()
            self.borrar()
        
        if self.SeleccionRegistro:
            messagebox.showinfo("Problema", "no se puede reingresar un registro que se encuentra en base de datos")
            self.borrar()

        


    
    def seleccionar(self):
        self.borrar()
        self.idItem=int(self.treeview.selection()[0])

        sql = "SELECT * FROM proveedores WHERE (id = '{}');".format(self.idItem)
        self.cursor.execute(sql)
        datos = self.cursor.fetchone()
        
        self.entradaEmpresa.insert(0,datos[1]) 
        self.entradaRepresentante.insert(0,datos[2])
        self.entradaNIT.insert(0,datos[3])
        self.entradaTelefono.insert(0,datos[11])
        self.comboBoxPyme.set(datos[4])
        self.comboBoxDepartamento.set(datos[5])
        self.comboBoxMunicipio.set(datos[6])
        self.entradaDireccion.insert(0,datos[7])
        self.comboBoxCategoria.set(datos[8])
        self.entradaDescripcion.insert(0,datos[9])
        self.labelRut.config(text= datos[10])

        self.SeleccionRegistro = True #el false muestra que se ha señalado un registro

    def eliminar(self):
        if ~self.SeleccionRegistro:  #si no se tiene seleccionado algun registro
            messagebox.showinfo("Problema", "se debe seleccionar un registro a eliminar")

        if self.SeleccionRegistro:
            sql = "DELETE FROM proveedores WHERE (id = '{}');".format(self.idItem)
            self.cursor.execute(sql)
            self.connection.commit()
            self.refrescar()
            self.borrar()

    def actualizar(self):
        valor = self.validar()
        if valor & self.SeleccionRegistro:
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

            if self.archivo != "":
                destino = "/Users/debbiearredondo/desktop/prueba"     #se debe guardar la ruta del destino de los RUT  <<<<<<< SE DEBE CAMBIAR !!!
                nombreRUT =os.path.basename(self.archivo)
                os.makedirs(destino, mode=0o777, exist_ok=True)
                shutil.copy(self.archivo, destino)        #hace una copia del archivo


            sql = "UPDATE proveedores SET Empresa = '{}',Representante = '{}',Nit= '{}',EsPyme= '{}',Departamento= '{}',Municipio= '{}',Direccion= '{}',Categoria= '{}',Descripcion= '{}',Telefono= '{}',Archivo= '{}' WHERE (id = '{}');".format(empresa,representante,nit,espyme,departamento,municipio,direccion,categoria,descripcion,telefono,nombreRUT,self.idItem)
            self.cursor.execute(sql)
            self.connection.commit()
            self.refrescar()
            self.borrar()
            self.SeleccionRegistro = False #el false muestra que no se ha señalado un registro

    def refrescar(self):
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT id,Empresa,Representante,Telefono,Departamento,Municipio,Categoria,Archivo FROM Proveedores"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
            n = n+1

    def validar(self): #valida si todos los elementos de la ventana se encuentran con valores en caso contrario no deja guardar la información
        valor = True
        if self.entradaEmpresa.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el nombre de la empresa")
            valor = False
        if self.entradaRepresentante.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el nombre del representante de la empresa")
            valor = False
        if self.entradaNIT.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el NIT del cliente")
            valor = False
        if self.entradaTelefono.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el telefono de la empresa")
            valor = False
        if self.comboBoxPyme.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar si la empresa es Pyme")
            valor = False
        if self.comboBoxDepartamento.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar el departamento")
            valor = False
        if self.comboBoxMunicipio.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar el municipio")
            valor = False
        if self.entradaDireccion.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar una direccion")
            valor = False
        if self.comboBoxCategoria.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar una categoria")
            valor = False
        if self.entradaDescripcion.get() == "":
            messagebox.showinfo("Problema", "se debe seleccionar una descripción")
            valor = False

        return valor

    def borrar(self):  #metodo para borrar los valores del formulario.
        self.entradaEmpresa.delete(0,tk.END)
        self.entradaRepresentante.delete(0,tk.END)
        self.entradaNIT.delete(0,tk.END)
        self.entradaTelefono.delete(0,tk.END)
        self.comboBoxPyme.set("")
        self.comboBoxDepartamento.set("")
        self.comboBoxMunicipio.set("")
        self.entradaDireccion.delete(0,tk.END)
        self.comboBoxCategoria.set("")
        self.entradaDescripcion.delete(0,tk.END)
        self.labelRut.config(text= "Vacio")

        self.SeleccionRegistro = False #cada vez que se borra el formulario se restablece la no selección de registros
    
    def adjuntarRUT(self):
        self.archivo = filedialog.askopenfilename()   #selecciona el archivo 
        self.labelRut.config(text= os.path.basename(self.archivo))
        
        
        

class treeViewDashboard(tk.Tk):
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
        self.frame2 = tk.Frame(master=self)
        self.frame3 = tk.Frame(master=self)
        self.frame1.grid(row=0,column=0,sticky="nsew")
        self.frame2.grid(row=1,column=0,sticky="nsew")
        self.frame3.grid(row=1,column=1,sticky="nsew")

        self.treeview = ttk.Treeview(master=self.frame1,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11'))
        self.treeview.grid(row = 0, column = 0,sticky="ew")

        
        #self.treeview.configure(xscrollcommand=self.scrollbarTree.set)
        
        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=50)  #id
        self.treeview.column('#1', width=150) #empresa
        self.treeview.column('#2', width=150) #representante
        self.treeview.column('#3', width=100) #nit
        self.treeview.column('#4', width=50)  #es pyme
        self.treeview.column('#5', width=130) #departamento
        self.treeview.column('#6', width=130) #municipio
        self.treeview.column('#7', width=200) #direccion
        self.treeview.column('#8', width=100) #categoria
        self.treeview.column('#9', width=150) #descripcion

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

        self.scrollbarTree = ttk.Scrollbar(master=self.frame1,orient="horizontal",command=self.treeview.xview)
        self.scrollbarTree.grid(row = 1, column = 0,sticky="ew")
        self.treeview.config(xscrollcommand=self.scrollbarTree.set)

        def filtrar(event):
            nombre = self.entradaEmpresa.get()
            
            self.treeview.delete(*self.treeview.get_children())

            sql = "SELECT * FROM Proveedores WHERE Empresa like '%{}%'".format(nombre)
            self.cursor.execute(sql)

            n=0
            for dato in self.cursor.fetchall():
                self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
                n = n+1
        
        # def nuevoFiltro(event):
        #     nombre = self.entradaRepresentante.get()
        #     self.treeview.delete(*self.treeview.get_children())

        #     sql = "SELECT * FROM Proveedores WHERE Representante like '%{}%'".format(nombre)
        #     self.cursor.execute(sql)

        #     n=0
        #     for dato in self.cursor.fetchall():
        #         self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
        #         n = n+1


        self.entradaEmpresa = tk.Entry(master = self.frame2, textvariable="Buscar:")
        self.entradaEmpresa.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.entradaEmpresa.bind('<Key>', filtrar)


        # self.entradaRepresentante = tk.Entry(master = self.frame2, textvariable="Representante:")
        # self.entradaRepresentante.grid(row = 0, column = 1, padx = 10, pady = 10)
        # self.entradaRepresentante.bind('<key>',nuevoFiltro)

        self.refrescar()
    
    def refrescar(self):
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT * FROM Proveedores"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
            n = n+1
    
    


if __name__ == "__main__":
    VentanaGastos = SeguimientoGastos()
    VentanaGastos.mainloop()