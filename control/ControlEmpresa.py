from control.ControlConexion import *
from control.configBd import *
from modelo.Empresa import *

class ControlEmpresa():
    """
    This class represents the control for managing clients.
    """

    def __init__(self, objEmpresa=None):
        """
        Initializes a new instance of the ControlEmpresa class.

        Args:
            objEmpresa: An object representing a Company (empresa)
        """
        self.objEmpresa = objEmpresa
    
    def listar(self):
        """
        Retrieves a list of Empresas.

        Returns:
            A list of Empresa objects.
        """
        arregloEmpresas = [] 
        msg = "ok"
        comandoSql = "SELECT * FROM empresa;"
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:         
                for fila in cursor:
                    objEmpresa = Empresa(0)
                    objEmpresa.setCodigo(fila[0])
                    objEmpresa.setNombre(fila[1])
                    arregloEmpresas.append(objEmpresa)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return arregloEmpresas
    
    def consultar(self):
        """
        Retrieves an Empresa based on the person's code.

        Returns:
            A Empresa object.
        """
        msg = "ok"
        cod = self.objEmpresa.getCodigo()
        comandoSql = "SELECT * FROM empresa WHERE codigo = '{}'".format(cod)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0: 
                for fila in cursor:
                    self.objEmpresa.setCodigo(fila[0])
                    self.objEmpresa.setNombre(fila[1])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)

        return self.objEmpresa

    def guardar(self):
        
        """
        Saves an Empresa information to the database.

        Returns:
            A message indicating the status of the operation.
        """
        msg = "ok"
        
        cod = self.objEmpresa.getCodigo() 
        nom = self.objEmpresa.getNombre()
        
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO empresa(codigo, nombre) VALUES('{}', '{}')".format(cod, nom)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()

        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
            
        return msg

    def borrar(self):
        """
        Deletes an Empresa information from the database.

        Returns:
            A message indicating the status of the operation.
        """
        cod = self.objEmpresa.getCodigo() 
        try:
            objControlConexion =  ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "UPDATE cliente SET fkcodempresa = Null WHERE fkcodempresa Like '{}';".format(cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM empresa WHERE codigo = '{}';".format(cod)
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
        """
        Modifies a Empresa's information in the database.
        """
        cod = self.objEmpresa.getCodigo()
        nom = self.objEmpresa.getNombre()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO empresa(codigo, nombre) VALUES ('{}', '{}') ON CONFLICT (codigo) DO UPDATE SET nombre = '{}'".format(cod, nom, nom)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
