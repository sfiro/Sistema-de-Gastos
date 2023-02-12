import mysql.connector
import pandas as pd

datos = pd.read_csv('/Users/debbiearredondo/desktop/gastos2.csv',sep=';',header=0)

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='3231213',
    db='INGENIO'
)

cursor = connection.cursor()
cursor.execute("SELECT database();")
registro = cursor.fetchone()

print("conexion establecida exitosamente")
print("la base de datos se llama:",registro)

 
#print(datos)

#------------tabla de detalle gastos -------------------
# sql = "CREATE TABLE DetalleGastos ( id INT AUTO_INCREMENT PRIMARY KEY, Tipo VARCHAR(30), Detalle VARCHAR(50));"
# cursor.execute(sql)

# for i in range(len(datos)): 
#     sql = "INSERT INTO DetalleGastos (Tipo,Detalle) VALUES ('{}','{}')".format(datos.loc[i,"tipo"],datos.loc[i,"detalle"])
#     cursor.execute(sql)

#------------tabla de gastos -------------------
# sql = "CREATE TABLE TipoGastos ( id INT AUTO_INCREMENT PRIMARY KEY, Tipo VARCHAR(30));"
# cursor.execute(sql)

# for i in range(len(datos)): 
#     print(datos.loc[i,"datos"])
#     sql = "INSERT INTO TipoGastos (Tipo) VALUES ('{}')".format(datos.loc[i,"datos"])
#     cursor.execute(sql)

#------------tabla de proveedores -------------------

# sql = "CREATE TABLE proveedores ( id INT AUTO_INCREMENT PRIMARY KEY, Empresa VARCHAR(100),Representante VARCHAR(100),Nit VARCHAR(30),EsPyme BOOLEAN,Departamento VARCHAR(100),Municipio VARCHAR(100),Direccion VARCHAR(100),Categoria VARCHAR(50),Descripcion VARCHAR(100),Archivo VARCHAR(100),Telefono VARCHAR(30));"
# cursor.execute(sql)

print(datos.loc[0,:])

# ingreso de datos en la tabla proveedores
# for i in range(len(datos)): 
#     sql = "INSERT INTO proveedores (Empresa,Representante,Nit,EsPyme,Departamento,Municipio,Direccion,Categoria,Descripcion,Archivo,Telefono) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(datos.loc[i,"Nombre Empresa"],
#                                     datos.loc[i,"Representante Legal"],datos.loc[i,"NIT"],datos.loc[i,"EsPyme"],datos.loc[i,"Departamento"],
#                                     datos.loc[i,"Municipio"],datos.loc[i,"Dirección"],datos.loc[i,"Categoria"],datos.loc[i,"Descripción"],
#                                     datos.loc[i,"Archivo"],datos.loc[i,"Telefono"])
#     cursor.execute(sql)



# CARGUE DE TODOS LOS DATOS EN LA BASE
# sql = "CREATE TABLE municipios ( id INT AUTO_INCREMENT PRIMARY KEY, departamento VARCHAR(255) NOT NULL,municipio VARCHAR(255) NOT NULL);"
# cursor.execute(sql)

# for i in range(len(datos)): 
#     sql = "INSERT INTO municipios (departamento,municipio) VALUES ('{}','{}')".format(datos.loc[i,"DEPARTAMENTO"],datos.loc[i,"MUNICIPIO"])
#     cursor.execute(sql)

connection.commit()


