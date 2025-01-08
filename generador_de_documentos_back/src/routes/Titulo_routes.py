from flask import Blueprint
from src.controllers.Titulo_controller import TituloController

def crear_rutas_titulo(mongo):
    # Crear el Blueprint de las rutas
    titulo_bp = Blueprint('titulo_bp', __name__)
    
    # Crear una instancia del controlador
    controller = TituloController(mongo)

    # Rutas
    @titulo_bp.route('/titulo', methods=['POST'])
    def crear_titulo():
        return controller.crear_titulo()

    @titulo_bp.route('/titulo', methods=['GET'])
    def obtener_titulos():
        return controller.obtener_titulos()

    @titulo_bp.route('/titulo/<id>', methods=['DELETE'])
    def eliminar_titulo(id):
        return controller.eliminar_titulo(id)
    

    return titulo_bp
