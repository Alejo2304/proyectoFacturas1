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