class Factura(object):
    def __init__(self, numero=None, fecha=None, total=None, cliente=None, vendedor=None):
        self.numero = numero
        self.fecha = fecha
        self.total = total
        self.cliente = cliente
        self.vendedor = vendedor

    def getNumero(self):
        return self.numero
    def setNumero(self, numero):
        self.numero = numero

    """
    The following SQL comand was used to change the data type of the column fecha from time to timestamp on the DATABASE
        ALTER TABLE factura 
        ALTER COLUMN fecha 
        TYPE timestamp 
        USING '2024-04-18';5
    """
    def getFecha(self):
        return self.fecha
    def setFecha(self, fecha):
        self.fecha = fecha

    def getTotal(self):
        return self.total
    def setTotal(self, total):
        self.total = total

    def getCliente(self):
        return self.cliente
    def setCliente(self, cliente):
        self.cliente = cliente

    def getVendedor(self):
        return self.vendedor
    def setVendedor(self, vendedor):
        self.vendedor = vendedor