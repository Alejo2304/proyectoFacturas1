from control.ControlConexion import *
from control.configBd import *
from modelo.Factura import Factura
class ControlFactura():

    def __init__(self, objFactura=None):
        self.objFactura = objFactura
    
    def listar(self): #Muestra los productos en la base de datos

        arregloFacturas = []
        msg = "ok"
        comandoSql = "SELECT * FROM factura"
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    objFactura = Factura(0)
                    objFactura.setNumero(fila[0])
                    objFactura.setFecha(fila[1])
                    objFactura.setTotal(fila[2])
                    objFactura.setCliente(fila[3])
                    objFactura.setVendedor(fila[4])
                    arregloFacturas.append(objFactura)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return arregloFacturas
    
    def consultar(self):
        msg = "ok"
        num = self.objFactura.getNumero()
        comandoSql = "SELECT * FROM factura WHERE factura.numero = '{}'".format(num)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:
                for fila in cursor:
                    self.objFactura = Factura(0)
                    self.objFactura.setNumero(fila[0])
                    self.objFactura.setFecha(fila[1])
                    self.objFactura.setTotal(fila[2])
                    self.objFactura.setCliente(fila[3])
                    self.objFactura.setVendedor(fila[4])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return self.objFactura
    
    def guardar(self):
        msg = "ok"
        num = self.objFactura.getNumero()
        fec = self.objFactura.getFecha()
        tot = self.objFactura.getTotal()
        cli = self.objFactura.getCliente()
        ven = self.objFactura.getVendedor()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
            comandoSql = "INSERT INTO factura(numero, fecha, total, fkidcliente, fkidvendedor) VALUES ('{}', '{}', '{}', '{}', '{}');".format(num, fec, tot, cli, ven)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)
            objControlConexion.cerrarBd()

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
    
    def borrar(self):
        num = self.objFactura.getNumero()
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM factura WHERE factura.numero = '{}'".format(num)
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

        num = self.objFactura.getNumero()
        fec = self.objFactura.getFecha()
        tot = self.objFactura.getTotal()
        cli = self.objFactura.getCliente()
        ven = self.objFactura.getVendedor()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO factura(numero, fecha, total, fkidcliente, fkidvendedor) VALUES ('{}', '{}', '{}', '{}', '{}');".format(num, fec, tot, cli, ven)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg