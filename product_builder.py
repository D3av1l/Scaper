# Objetos Productos
class Product:
    def __init__(self, nombre, precio, descripcion, indicaciones, composicion, modo_empleo):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.indicacciones = indicaciones
        self.composicion = composicion
        self.modo_empleo = modo_empleo
        
#getters
    def get_nombre(self):
        return self.nombre
    
    def get_precio(self):
        return self.precio
    
    def get_descripcion(self):
        return self.descripcion
    
    def get_indicaciones(self):
        return self.indicaciones
    
    def get_composicion(self):
        return self.composicion
    
    def get_modo_empleo(self):
        return self.modo_empleo
    
#setters
    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def set_precio(self, precio):
        self.precio = precio
    
    def set_descripcion(self, descripcion):
        self.descripcion = descripcion
    
    def set_indicaciones(self, indicaciones):
        self.indicaciones = indicaciones
    
    def set_composicion(self, composicion):
        self.composicion = composicion
    
    def set_modo_empleo(self, modo_empleo):
        self.modo_empleo = modo_empleo    
