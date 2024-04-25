from modelo.Persona import Persona
#DE modelo.Persona IMPORTAR LA CLASE PERSONA
#Hay que añadir clave foranea para relacionar empresas. 
class Cliente(Persona):
    def __init__(self,credito=None, empresa=None):
        self.credito=credito
        self.empresa=empresa

    def setcredito(self,credito=None):
        self.credito=credito
    def getCredito(self):
        return self.credito

    def setEmpresa(self,empresa=None):
        self.empresa=empresa
    def getEmpresa(self):
        return self.empresa