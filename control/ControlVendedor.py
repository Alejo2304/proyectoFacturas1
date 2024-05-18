from control.ControlConexion import *
from control.configBd import *
from modelo.Vendedor import *
class ControlVendedor():
    """
    This class represents the control for managing Vendedores.
    """

    def __init__(self, objPersona=None, objVendedor=None):
        """
        Initializes a new instance of the ControlVendedor class.

        Args:
            objPersona: An object representing a person.
            objVendedor: An object representing a Vendedor.
        """
        self.objPersona = objPersona
        self.objVendedor = objVendedor
    
    def listar(self):
        """
        Retrieves a list of Vendedores.

        Returns:
            A list of Vendedores objects.
        """
        arregloVendedores = [] 
        msg = "ok"
        comandoSql = "SELECT * FROM persona inner join vendedor on vendedor.fkcodpersona=persona.codigo"
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0:         
                for fila in cursor:
                    objVendedor = Vendedor(0)
                    objVendedor.setCodigo(fila[0])
                    objVendedor.setNombre(fila[1])
                    objVendedor.setEmail(fila[2]) #corrected bug with setEmail and setTelefono
                    objVendedor.setTelefono(fila[3])
                    objVendedor.setCarnet(fila[5])
                    objVendedor.setDireccion(fila[6])
                    arregloVendedores.append(objVendedor)
            objControlConexion.cerrarBd()
            
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return arregloVendedores
    
    def consultar(self):
        """
        Retrieves a Vendedor based on the person's code.

        Returns:
            A Vendedor object.
        """
        msg = "ok"
        cod = self.objPersona.getCodigo()
        comandoSql = "SELECT * FROM persona inner join vendedor on vendedor.fkcodpersona=persona.codigo where codigo  = '{}'".format(cod)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0: 
                for fila in cursor:           
                    self.objVendedor = Vendedor(0)
                    self.objVendedor.setCodigo(fila[0])
                    self.objVendedor.setNombre(fila[1])
                    self.objVendedor.setEmail(fila[2]) #corrected bug with setEmail and setTelefono
                    self.objVendedor.setTelefono(fila[3])
                    self.objVendedor.setCarnet(fila[5])
                    self.objVendedor.setDireccion(fila[6])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)

        return self.objVendedor
    
    def consultarPorVendedor(self, IdVendedor):
        msg = "ok"
        comandoSql = "SELECT * FROM persona inner join vendedor on vendedor.fkcodpersona=persona.codigo where vendedor.id = '{}'".format(IdVendedor)
        objControlConexion = ControlConexion()
        msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if cursor.rowcount > 0: 
                for fila in cursor:           
                    self.objVendedor = Vendedor(0)
                    self.objVendedor.setCodigo(fila[0])
                    self.objVendedor.setNombre(fila[1])
                    self.objVendedor.setEmail(fila[2]) #corrected bug with setEmail and setTelefono
                    self.objVendedor.setTelefono(fila[3])
                    self.objVendedor.setCarnet(fila[5])
                    self.objVendedor.setDireccion(fila[6])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)

        return self.objVendedor

    def guardar(self):
        
        """
        Saves a client and person information to the database.

        Returns:
            A message indicating the status of the operation.
        """
        msg = "ok"
        
        cod = self.objPersona.getCodigo() 
        nom = self.objPersona.getNombre()
        tel = self.objPersona.getTelefono() 
        ema = self.objPersona.getEmail()
        car = self.objVendedor.getCarnet()
        dir = self.objVendedor.getDireccion()

        #        
        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO persona(codigo, nombre, telefono, email) VALUES ('{}', '{}', '{}', '{}')".format(cod, nom, tel, ema)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "INSERT INTO vendedor(carnet, direccion, fkcodpersona) VALUES ({}, '{}', '{}')".format(car,dir,cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()

        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
            
        return msg

    def borrar(self):
        """
        Deletes a vendedor and person information from the database.

        Returns:
            A message indicating the status of the operation.
        """
        cod = self.objPersona.getCodigo() 
        try:
            objControlConexion =  ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM vendedor WHERE fkcodpersona = '{}';".format(cod);
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM persona WHERE codigo = '{}';".format(cod)
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
        Modifies a Vendedor's information in the database.
        """
        cod = self.objPersona.getCodigo()
        nom = self.objPersona.getNombre()
        tel = self.objPersona.getTelefono()
        ema = self.objPersona.getEmail()
        car = self.objVendedor.getCarnet()
        dir = self.objVendedor.getDireccion()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO persona (codigo, nombre, telefono, email) VALUES ('{}', '{}', '{}', '{}') ON CONFLICT (codigo) DO UPDATE SET nombre = '{}', telefono = '{}', email = '{}'".format(cod, nom, tel, ema, nom, tel, ema)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "INSERT INTO vendedor(fkcodpersona, carnet, direccion) VALUES ('{}', '{}', '{}') ON CONFLICT (fkcodpersona) DO UPDATE SET carnet = '{}', direccion = '{}'".format(cod, car, dir, car, dir)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg
