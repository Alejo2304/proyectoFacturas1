from control.ControlConexion import *
from control.configBd import *
from modelo.Producto import Producto
class ControlProducto():

    def __init__(self, objProducto=None):
        self.objProducto = objProducto
    
    def listar(self): #Muestra los productos en la base de datos

        arregloProductos = []
        msg = "ok"
        comandoSql = "SELECT * FROM producto"
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    objProducto = Producto(0)
                    objProducto.setCodigo(fila[0])
                    objProducto.setNombre(fila[1])
                    objProducto.setStock(fila[2])
                    objProducto.setValorUnitario(fila[3])
                    arregloProductos.append(objProducto)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return arregloProductos
    
    def consultar(self):
        msg = "ok"
        cod = self.objProducto.getCodigo()
        comandoSql = "SELECT * FROM producto where codigo = '{}'".format(cod)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    self.objProducto = Producto(0)
                    self.objProducto.setCodigo(fila[0])
                    self.objProducto.setNombre(fila[1])
                    self.objProducto.setStock(fila[2])
                    self.objProducto.setValorUnitario(fila[3])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return self.objProducto
    
    def guardar(self):
        msg = "ok"
        cod = self.objProducto.getCodigo()
        nom = self.objProducto.getNombre()
        sto = self.objProducto.getStock()
        val = self.objProducto.getValorUnitario()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
            comandoSql = "INSERT INTO producto (codigo, nombre, stock, valorunitario) VALUES ('{}', '{}', '{}', '{}');".format(cod, nom, sto, val)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)
            objControlConexion.cerrarBd()

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
    
    def borrar(self):
        cod = self.objProducto.getCodigo()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM productosporfactura WHERE fkcodproducto = '{}'".format(cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM producto WHERE codigo = '{}'".format(cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "END;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
    
    def modificar(self):

        cod = self.objProducto.getCodigo()
        nom = self.objProducto.getNombre()
        sto = self.objProducto.getStock()
        val = self.objProducto.getValorUnitario()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO producto (codigo, nombre, stock, valorunitario) VALUES ('{}', '{}', '{}', '{}') ON CONFLICT (codigo) DO UPDATE SET nombre = '{}', stock = '{}', valorunitario = '{}'".format(cod, nom, sto, val, nom, sto, val)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg