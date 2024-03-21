class Producto(object):
    def __init__(self, codigo=None, nombre=None, stock=None, valorunitario=None):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock
        self.valorunitario = valorunitario

    def setCodigo(self, codigo):
        self.codigo = codigo
    def getCodigo(self):
        return self.codigo
    
    def setNombre(self, nombre):
        self.nombre = nombre
    def getNombre(self):
        return self.nombre
    
    def setValorUnitario(self, valorunitario):
        self.valorunitario = valorunitario
    def getValorUnitario(self):
        return self.valorunitario
    
    def setStock(self, stock):
        self.stock = stock
    def getStock(self):
        return self.stock
    
# Path: proyectoFacturas1/modelo/Producto.py