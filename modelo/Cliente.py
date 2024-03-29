from modelo.Persona import Persona
#DE modelo.Persona IMPORTAR LA CLASE PERSONA
class Cliente(Persona):
    def __init__(self,credito=None):
        self.credito=credito

    def setcredito(self,credito=None):
        self.credito=credito
    def getCredito(self):
        return self.credito
