class Rol():
    def __init__(self,id=None,nombre=None):
        self.id=id
        self.nombre=nombre

    def setId(self,id):
        self.id=id
    def getId(self):
        return self.id

    def setNombre(self,nombre):
        self.nombre=nombre
    def getNombre(self):
        return self.nombre