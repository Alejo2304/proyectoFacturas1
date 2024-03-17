from modelo.Persona import Persona
class Vendedor(Persona):
    def __init__(self,carnet=None, direccion=None):
        self.carnet=carnet
        self.direccion=direccion

    def setCarnet(self, carnet):
        self.carnet = carnet
    def getCarnet(self):
        return self.carnet

    def setDireccion(self, direccion):
        self.direccion = direccion
    def getDireccion(self):
        return self.direccion
