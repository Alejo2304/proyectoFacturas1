from control.ControlConexion import *
from control.configBd import *
from modelo.ProductosPorFactura import ProductosPorFactura
class ControlProductosPorFactura():

    def __init__(self, objProductosPorFactura=None):
        self.objProductosPorFactura = objProductosPorFactura
    
    def listar(self): #Muestra los productos en la base de datos

        arregloProductosPorFacturas = []
        msg = "ok"
        comandoSql = "SELECT * FROM productosporfactura"
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    objProductosPorFactura = ProductosPorFactura(0)
                    objProductosPorFactura.setFactura(fila[0])
                    objProductosPorFactura.setProducto(fila[1])
                    objProductosPorFactura.setCantidad(fila[2])
                    objProductosPorFactura.setSubtotal(fila[3])
                    arregloProductosPorFacturas.append(objProductosPorFactura)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return arregloProductosPorFacturas
    
    def consultar(self):
        msg = "ok"
        fac = self.objProductosPorFactura.getFactura()
        pro = self.objProductosPorFactura.getProducto()
        comandoSql = "SELECT * FROM productosporfactura WHERE fknumfactura = '{}' AND fkcodproducto = '{}'".format(fac, pro)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    self.objProductosPorFactura = ProductosPorFactura(0)
                    self.objProductosPorFactura.setFactura(fila[0])
                    self.objProductosPorFactura.setProducto(fila[1])
                    self.objProductosPorFactura.setCantidad(fila[2])
                    self.objProductosPorFactura.setSubtotal(fila[3])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return self.objProductosPorFactura
    
    def guardar(self):
        msg = "ok"
        fac = self.objProductosPorFactura.getFactura()
        pro = self.objProductosPorFactura.getProducto()
        can = self.objProductosPorFactura.getCantidad()
        sub = self.objProductosPorFactura.getSubtotal()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
            comandoSql = "INSERT INTO productosporfactura(fknumfactura, fkcodproducto, cantidad, subtotal) VALUES ('{}', '{}', '{}', '{}')".format(fac, pro, can, sub)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)
            objControlConexion.cerrarBd()

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
     
    def borrar(self):
        fac = self.objProductosPorFactura.getFactura()
        pro = self.objProductosPorFactura.getProducto()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM productosporfactura WHERE fknumfactura = '{}' AND fkcodproducto = '{}'".format(fac, pro)
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

        fac = self.objProductosPorFactura.getFactura()
        pro = self.objProductosPorFactura.getProducto()
        can = self.objProductosPorFactura.getCantidad()
        sub = self.objProductosPorFactura.getSubtotal()
        
        try:
            objControlConexion = ControlConexion()

            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
            
            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM productosporfactura WHERE fknumfactura = '{}' AND fkcodproducto = '{}'".format(fac, pro)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "INSERT INTO productosporfactura(fknumfactura, fkcodproducto, cantidad, subtotal) VALUES ('{}', '{}', '{}', '{}')".format(fac, pro, can, sub)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "END;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)


            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg