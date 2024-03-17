class Empresa(object):
    def __init__(self,codigo=None,nombre=None):
        self.codigo=codigo
        self.nombre=nombre

    def setCodigo(self,codigo = None):
        self.codigo=codigo
    def getCodigo(self):
        return self.codigo

    def setNombre(self,nombre=None):
        self.nombre=nombre
    def getNombre(self):
        return self.nombre