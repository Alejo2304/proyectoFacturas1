class ProductosPorFactura(object):
    def __init__(self, factura=None, producto=None, cantidad=None, subtotal=None):
        self.factura = factura
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = subtotal

    def getFactura(self):
        return self.factura
    def setFactura(self, factura):
        self.factura = factura

    def getProducto(self):
        return self.producto
    def setProducto(self, producto):
        self.producto = producto

    def getCantidad(self):
        return self.cantidad
    def setCantidad(self, cantidad):
        self.cantidad = cantidad

    def getSubtotal(self):
        return self.subtotal
    def setSubtotal(self, subtotal):
        self.subtotal = subtotal

    