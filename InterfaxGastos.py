import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog     #importante para tener ventanas de busqueda de archivos
import mysql.connector
import shutil   #necesario para copiar archivos
import os     #necesario para crear carpetas
import datetime   #modulo necesario para manejar fecha 




class compartir:  
    # ---------------------- funcion para buscar compartir valores entre interfaces  ---------------------------------
    def __init__(self):
        self.idProveedor = None

# -------------------- Ventana Principal del modulo de gasto ---------------------------------------
class SeguimientoGastos(tk.Tk):
    def __init__(self,datos):
        super().__init__()

        self.datos = datos

        self.title("Seguimiento Gastos")
        self.geometry("500x300")

        self.ingresarButton = tk.Button(master=self,text="Agregar Gasto",command=self.gastos)
        self.ingresarButton.grid(row=0,column=0,padx=10,pady=10)
        self.actualizarButton = tk.Button(master=self,text="Agregar Proveedor",command=self.proveedor)
        self.actualizarButton.grid(row=1,column=0,padx=10,pady=10)
        self.treeviewButton = tk.Button(master=self,text="Seleccionar Proveedor",command=self.tree)
        self.treeviewButton.grid(row=2,column=0,padx=10,pady=10)
        self.visorGastosButton = tk.Button(master=self,text="Visor de Gastos",command=self.visorGastos)
        self.visorGastosButton.grid(row=3,column=0,padx=10,pady=10)
    
    def gastos(self):
        agregar = AgregarGastos(self.datos)
        agregar.mainloop()

    def proveedor(self):
        proveedorIngreso = AgregarProveedor()
        proveedorIngreso.mainloop()
    
    def tree(self):
        treeView = treeViewDashboard(self.datos)
        treeView.mainloop()

    def visorGastos(self):
        visor = VisorGastos()
        visor.mainloop()



# -------------------- Ventana secundaria del modulo de gasto (agregar gasto)---------------------------------------
class AgregarGastos(tk.Tk):
    def __init__(self, datos):
        super().__init__()

        self.datos = datos

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

        self.title("Agregar Gasto")
        self.geometry("900x550")

        self.frame1 = tk.Frame(master=self)
        self.frame2 = tk.Frame(master=self)
        self.frame3 = tk.Frame(master=self)
        self.frame1.grid(row=0,column=0,sticky="nsew")
        self.frame2.grid(row=1,column=0,sticky="nsew")
        self.frame3.grid(row=2,column=0,sticky="nsew")
        #self.frame1.columnconfigure(0,weight=0)
        #self.frame1.columnconfigure(1,weight=0)

# ------------------------- Label de la interfax para agregar gastos -----------------------------------------------------
        self.tipoGastoLabel = tk.Label(master = self.frame1, text = "Tipo de gasto:")
        self.tipoGastoLabel.grid(row = 0, column = 0, padx = 10, pady = 5)

        self.detalleGastoLabel = tk.Label(master = self.frame1, text = "Detalle de gasto:")
        self.detalleGastoLabel.grid(row = 1, column = 0, padx = 10, pady = 5)

        self.descripcionGastoLabel = tk.Label(master = self.frame1, text = "Descripción Gasto:")
        self.descripcionGastoLabel.grid(row = 2, column = 0, padx = 10, pady = 5)

        self.seleccionarButton = tk.Button(master=self.frame1,text="Seleccionar proveedor",command=self.seleccionar)
        self.seleccionarButton.grid(row=3,column=0,padx=10,pady=10)

        self.seleccionarFechaButton = tk.Button(master=self.frame1,text="Seleccionar Fecha",command=self.seleccionarFecha)
        self.seleccionarFechaButton.grid(row=4,column=0,padx=10,pady=10)

        self.valorGastoLabel = tk.Label(master = self.frame1, text = "Valor de gasto:")
        self.valorGastoLabel.grid(row = 5, column = 0, padx = 10, pady = 5)


        

# ------------------------- Elementos de interación de la interfax gráfica para agregar gastos ---------------------

        self.tipoGastoComboBox = ttk.Combobox(master = self.frame1)
        #self.comboBoxTipoGasto['values'] = ("SI","NO")
        self.tipoGastoComboBox.grid(row = 0, column = 1, padx = 10, pady = 5)

        def seleccion(event): #evento que actuliza la base de datos del combobox detalle de gastos en base a la seleccion del tipo de gasto
    
            sql = "SELECT Detalle FROM DetalleGastos WHERE Tipo = '{}';".format(self.tipoGastoComboBox.get())  
            self.cursor.execute(sql)
            valores =[]
            for valor in self.cursor.fetchall():
                valores.append(valor[0])
            self.detalleGastoComboBox['values'] = valores

        sql = "SELECT Tipo FROM TipoGastos " 
        self.cursor.execute(sql)
        valores =[]
        for valor in self.cursor.fetchall():
            valores.append(valor[0])
        self.tipoGastoComboBox['values'] = valores
        self.tipoGastoComboBox.bind("<<ComboboxSelected>>",seleccion) #este es un evento que ocurre al generar un cambio en el combobox tipo de gasto

        self.detalleGastoComboBox = ttk.Combobox(master = self.frame1)
        #self.comboBoxTipoGasto['values'] = ("SI","NO")
        self.detalleGastoComboBox.grid(row = 1, column = 1, padx = 10, pady = 5)

        self.descripcionEntry = tk.Entry(master = self.frame1, text = "Direccion:")
        #self.descripcionEntry.grid(row = 2, column = 1, rowspan=2, padx = 10, pady = 5,sticky="nsew") # mirar esta versión 
        self.descripcionEntry.grid(row = 2, column = 1, padx = 10, pady = 5,sticky="nsew")

        self.proveedorLabel = tk.Label(master = self.frame1, text = "")
        self.proveedorLabel.grid(row = 3, column = 1, padx = 10, pady = 5)

        self.fechaLabel = tk.Label(master = self.frame1, text = "")
        self.fechaLabel.grid(row = 4, column = 1, padx = 10, pady = 5)

        self.valorGastoEntry = tk.Entry(master = self.frame1, text = "Pago:")
        self.valorGastoEntry.grid(row = 5, column = 1, padx = 10, pady = 5,sticky="nsew")

        #########  

        def filtrar(event):   #evento al momento de apretar enter en el valor 
            
            self.valorGasto = float(self.valorGastoEntry.get())
            formatted_num = "{:,.1f}".format(self.valorGasto) # Formatear el número con 2 decimales y separadores de miles
            #print(formatted_num)
            self.valorGastoEntry.delete(0,tk.END)   #borra el entry 
            self.valorGastoEntry.insert(0,formatted_num)   #cambia los valores por el formato
            
        
        self.valorGastoEntry = tk.Entry(master = self.frame1, text = "Pago:")
        self.valorGastoEntry.grid(row = 5, column = 1, padx = 10, pady = 5,sticky="nsew")
        self.valorGastoEntry.bind('<Return>', filtrar)  #evento que se activa cuando se apreta el boton enter 

# --------Botones del frame 2 ------ para guardar y borrar datos de la interfax
        
        self.guardarButton = tk.Button(master=self.frame2,text="Guardar",command=self.guardar)
        self.guardarButton.grid(row=0,column=0,padx=10,pady=10)

        self.borrarButton = tk.Button(master=self.frame2,text="Borrar formulario",command=self.eliminar)
        self.borrarButton.grid(row=0,column=1,padx=10,pady=10)

        self.cargarButton = tk.Button(master=self.frame2,text="cargar",command=self.cargar)
        self.cargarButton.grid(row=0,column=2,padx=10,pady=10)

        self.actualizarButton = tk.Button(master=self.frame2,text="actualizar",command=self.actualizar)
        self.actualizarButton.grid(row=0,column=3,padx=10,pady=10)

# ------- Treeview del Frame 3 ------------------------------

        self.treeview = ttk.Treeview(master=self.frame3,columns=('col1','col2','col3','col4','col5','col6','col7'))
        self.treeview.grid(row = 0, column = 0,sticky="ew")

        
        #self.treeview.configure(xscrollcommand=self.scrollbarTree.set)
        
        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=50)  #id
        self.treeview.column('#1', width=150) #empresa
        self.treeview.column('#2', width=150) #representante
        self.treeview.column('#3', width=150) #nit
        self.treeview.column('#4', width=150)  #es pyme
        self.treeview.column('#5', width=100) #departamento
        self.treeview.column('#6', width=150) #municipio
     

        self.treeview.heading('col1', text='tipo Gasto')
        self.treeview.heading('col2', text='detalle Gasto')
        self.treeview.heading('col3', text='descripcion Gasto')
        self.treeview.heading('col4', text='id Proveedor')
        self.treeview.heading('col5', text='fecha')
        self.treeview.heading('col6', text='valor Gasto')
        

        self.scrollbarTree = ttk.Scrollbar(master=self.frame3,orient="horizontal",command=self.treeview.xview)
        self.scrollbarTree.grid(row = 1, column = 0,sticky="ew")
        self.treeview.config(xscrollcommand=self.scrollbarTree.set)


        self.SeleccionRegistro = False
        self.refrescar()
    
    def validar(self): #valida si todos los elementos de la ventana se encuentran con valores en caso contrario no deja guardar la información
        valor = True
        
        if self.tipoGastoComboBox.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el tipo de gasto")
            valor = False
        if self.detalleGastoComboBox.get() == "":
            messagebox.showinfo("Problema", "se debe ingresar el detalle del gasto")
            valor = False
        if self.descripcionEntry.get() == "": 
            messagebox.showinfo("Problema", "se debe ingregar una descripción del gasto realizado")
            valor = False
        if self.proveedorLabel.cget("text") == "":
            messagebox.showinfo("Problema", "se debe seleccionar un proveedor")
            valor = False
        if self.fechaLabel.cget("text") == "":
            messagebox.showinfo("Problema", "se debe seleccionar una fecha")
            valor = False
        if self.valorGastoEntry.get() == "":
            messagebox.showinfo("Problema", "se debe agregar un valor para el gasto realizado")
            valor = False
        return valor
        
    def guardar(self):
        valor = self.validar()
        if valor & ~self.SeleccionRegistro:
            tipoGasto = self.tipoGastoComboBox.get()
            detalleGasto = self.detalleGastoComboBox.get()
            descripcionGasto = self.descripcionEntry.get()
            idProveedor = int(self.proveedorLabel.cget("text"))
            #fecha = datetime(self.fechaLabel.cget("text"))
            valorGasto = self.valor

            self.cursor.execute("INSERT INTO Gastos(tipoGasto,detalleGasto,descripcionGasto,idProveedor,fecha,valorGasto) VALUES('{}','{}','{}','{}','{}','{}');".format(tipoGasto,detalleGasto,descripcionGasto,idProveedor,datetime.date.today(),valorGasto))
            self.connection.commit()
            self.eliminar()
            self.refrescar()
        
            

    def eliminar(self):
        self.tipoGastoComboBox.set("")
        self.detalleGastoComboBox.set("")
        self.descripcionEntry.delete(0,tk.END)
        self.proveedorLabel.config(text= "")
        self.fechaLabel.config(text= "")
        self.valorGastoEntry.delete(0,tk.END)
        self.SeleccionRegistro = False

    def cargar(self):
        self.eliminar()
        self.idItem=int(self.treeview.selection()[0])

        sql = "SELECT * FROM Gastos WHERE (idGastos = '{}');".format(self.idItem)
        self.cursor.execute(sql)
        datos = self.cursor.fetchone()
        
        self.tipoGastoComboBox.set(datos[1])
        self.detalleGastoComboBox.set(datos[2])
        self.descripcionEntry.insert(0,datos[3]) 
        self.proveedorLabel.config(text= datos[4])
        self.fechaLabel.config(text= datos[5])
        self.valorGastoEntry.insert(0,datos[6]) 
        self.SeleccionRegistro = True

    def refrescar(self):
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT * FROM Gastos"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
            n = n+1

        self.proveedorLabel.configure(text=self.datos.idProveedor)

    def actualizar(self):
        valor = self.validar()
        if valor & self.SeleccionRegistro:
            tipoGasto = self.tipoGastoComboBox.get()
            detalleGasto = self.detalleGastoComboBox.get()
            descripcionGasto = self.descripcionEntry.get()
            idProveedor = int(self.proveedorLabel.cget("text"))
            #fecha = datetime(self.fechaLabel.cget("text"))
            valorGasto = self.valorGastoEntry.get()

            sql = "UPDATE Gastos SET tipoGasto = '{}',detalleGasto = '{}',descripcionGasto= '{}',idProveedor= '{}',fecha= '{}',valorGasto= '{}' WHERE (idGastos = '{}');".format(tipoGasto,detalleGasto,descripcionGasto,idProveedor,datetime.date.today(),valorGasto,self.idItem)
            self.cursor.execute(sql)
            self.connection.commit()
            self.refrescar()
            self.eliminar()
            self.SeleccionRegistro = False #el false muestra que no se ha señalado un registro


    def seleccionar(self):
        self.destroy()
        tree = treeViewDashboard(self.datos)
        tree.mainloop()

        #print(self.datos.idProveedor)


    def seleccionarFecha(self):
         self.fechaLabel.configure(text=datetime.date.today())

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
        self.geometry("1000x900")

        #self.columnconfigure(0, weight=1, minsize=70)

        self.frame1 = tk.Frame(master=self)
        self.frame1.grid(row=0,column=0,sticky="nsew")
        self.frame1.columnconfigure(0,weight=0)
        self.frame1.columnconfigure(1,weight=0)

        

        self.frame2 = tk.Frame(master=self)
        self.frame2.grid(row=1,column=0,sticky="nsew")
        self.frame2.columnconfigure(0,weight=1)
        self.frame2.columnconfigure(1,weight=1)
        self.frame2.columnconfigure(2,weight=1)
        self.frame2.columnconfigure(3,weight=1)

        self.frame3 = tk.Frame(master=self)
        self.frame3.grid(row=2,column=0,sticky="nsew")
        self.frame3.columnconfigure(0,weight=1)

# ------------------ label de la ventana proveedores -------------------------------------

        self.empresa = tk.Label(master = self.frame1, text = "Empresa:")
        self.empresa.grid(row = 0, column = 0, padx = 10, pady = 5)

        self.representante = tk.Label(master = self.frame1, text = "Representante legal:")
        self.representante.grid(row = 1, column = 0, padx = 10, pady = 5)

        self.nit = tk.Label(master = self.frame1, text = "NIT:")
        self.nit.grid(row = 2, column = 0, padx = 10, pady = 5)

        self.celular = tk.Label(master = self.frame1, text = "Celular:")
        self.celular.grid(row = 3, column = 0, padx = 10, pady = 5)

        self.pyme = tk.Label(master = self.frame1, text = "Es PYME:")
        self.pyme.grid(row = 4, column = 0, padx = 10, pady = 5)

        self.departamento = tk.Label(master = self.frame1, text = "Departamento:")
        self.departamento.grid(row = 5, column = 0, padx = 10, pady = 5)

        self.municipio = tk.Label(master = self.frame1, text = "Municipio:")
        self.municipio.grid(row = 6, column = 0, padx = 10, pady = 5)

        self.direccion= tk.Label(master = self.frame1, text = "Direccion:")
        self.direccion.grid(row = 7, column = 0, padx = 10, pady = 5)

        self.categoria = tk.Label(master = self.frame1, text = "Categoria:")
        self.categoria.grid(row = 8, column = 0, padx = 10, pady = 5)

        self.descripcion = tk.Label(master = self.frame1, text = "Descripcion:")
        self.descripcion.grid(row = 9, column = 0, padx = 10, pady = 5)

        self.rutButton = tk.Button(master=self.frame1,text="Adjuntar RUT",command=self.adjuntarRUT)
        self.rutButton.grid(row=10,column=0,padx=10,pady=5)

# ------------------ Entry de la ventana proveedores -------------------------------------

        self.entradaEmpresa = tk.Entry(master = self.frame1, textvariable="Empresa:")
        self.entradaEmpresa.grid(row = 0, column = 1, padx = 10, pady = 5)

        self.entradaRepresentante = tk.Entry(master = self.frame1, textvariable="Representante:")
        self.entradaRepresentante.grid(row = 1, column = 1, padx = 10, pady = 5)

        self.entradaNIT = tk.Entry(master = self.frame1, textvariable="NIT:")
        self.entradaNIT.grid(row = 2, column = 1, padx = 10, pady = 5)

        self.entradaTelefono = tk.Entry(master = self.frame1, textvariable="Telefono:")
        self.entradaTelefono.grid(row = 3, column = 1, padx = 10, pady = 5)

        self.comboBoxPyme = ttk.Combobox(master = self.frame1)
        self.comboBoxPyme['values'] = ("SI","NO")
        self.comboBoxPyme.grid(row = 4, column = 1, padx = 10, pady = 5)

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
        self.comboBoxDepartamento.grid(row = 5, column = 1, columnspan=2, padx = 10, pady = 5)
        self.comboBoxDepartamento.bind("<<ComboboxSelected>>",seleccion) #este es un evento que ocurre al generar un cambo en el combobox departamento

# ---- El valor seleccionado en departamento debe filtrar las opciones del combobox de municipios
        self.comboBoxMunicipio = ttk.Combobox(master = self.frame1)
        self.comboBoxMunicipio.grid(row = 6, column = 1, padx = 10, pady = 5)

        self.entradaDireccion = tk.Entry(master = self.frame1, text = "Direccion:")
        self.entradaDireccion.grid(row = 7, column = 1, padx = 10, pady = 5)

        self.comboBoxCategoria = ttk.Combobox(master = self.frame1)
        self.comboBoxCategoria['values'] = ("Madera","Impresiones")
        self.comboBoxCategoria.grid(row = 8, column = 1, padx = 10, pady = 5)

        self.entradaDescripcion = tk.Entry(master = self.frame1, text = "descripcion:")
        self.entradaDescripcion.grid(row = 9, column = 1, padx = 10, pady = 5)

        self.labelRut = tk.Label(master = self.frame1, text = "Vacio")
        self.labelRut.grid(row = 10, column = 1, padx = 10, pady = 5)

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

        self.archivo = ""  #necesario inicializar esta variable necesaria en el metodo de actualizacion para el nombreRUT

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
            else:
                nombreRUT = self.labelRut.cget("text")

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
    def __init__(self,datos):
        super().__init__()
        self.datos = datos
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

        self.refrescar()

        self.seleccionarButton = tk.Button(master=self.frame2,text="seleccionar",command=self.seleccionar)
        self.seleccionarButton.grid(row=1,column=0,padx=10,pady=10)

    
    def refrescar(self):
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT * FROM Proveedores"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
            n = n+1
    
    def seleccionar(self):
        self.idItem=int(self.treeview.selection()[0])
        self.datos.idProveedor = self.idItem
        self.destroy()
        # return self.datos.idProveedor

class VisorGastos(tk.Tk):
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

        self.treeview = ttk.Treeview(master=self.frame1,columns=('col1','col2','col3','col4','col5','col6','col7'))
        self.treeview.grid(row = 0, column = 0,sticky="ew")

        
        #self.treeview.configure(xscrollcommand=self.scrollbarTree.set)
        
        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=50)  #id
        self.treeview.column('#1', width=150) #empresa
        self.treeview.column('#2', width=150) #representante
        self.treeview.column('#3', width=150) #nit
        self.treeview.column('#4', width=150)  #es pyme
        self.treeview.column('#5', width=100) #departamento
        self.treeview.column('#6', width=150) #municipio
     

        self.treeview.heading('col1', text='tipo Gasto')
        self.treeview.heading('col2', text='detalle Gasto')
        self.treeview.heading('col3', text='descripcion Gasto')
        self.treeview.heading('col4', text='id Proveedor')
        self.treeview.heading('col5', text='fecha')
        self.treeview.heading('col6', text='valor Gasto')
        

        self.scrollbarTree = ttk.Scrollbar(master=self.frame1,orient="horizontal",command=self.treeview.xview)
        self.scrollbarTree.grid(row = 1, column = 0,sticky="ew")
        self.treeview.config(xscrollcommand=self.scrollbarTree.set)

     
        def filtrar(event):
            nombre = self.busquedaGasto.get()
            
            self.treeview.delete(*self.treeview.get_children())

            sql = "SELECT * FROM Gastos WHERE tipoGasto like '%{}%'".format(nombre)
            self.cursor.execute(sql)

            n=0
            for dato in self.cursor.fetchall():
                self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
                n = n+1


        self.busquedaGasto = tk.Entry(master = self.frame2, textvariable="Buscar:")
        self.busquedaGasto.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.busquedaGasto.bind('<Key>', filtrar)

        self.refrescar()

    

    
    def refrescar(self):
        self.treeview.delete(*self.treeview.get_children())
        sql = "SELECT * FROM Gastos"
        self.cursor.execute(sql)

        n=0
        for dato in self.cursor.fetchall():
            self.treeview.insert('','end',dato[0],text=dato[0],values=(dato[1:]))
            n = n+1
    
    

if __name__ == "__main__":
    datos = compartir()
    VentanaGastos = SeguimientoGastos(datos)
    VentanaGastos.mainloop()