from flask import Blueprint
from src.controllers.MetodoPico_controller import MetodoPicoController

def crear_rutas_metodoPico(mongo):
    # Crear el Blueprint de las rutas
    metodoPico_bp = Blueprint('metodoPico_bp', __name__)
    
    # Crear una instancia del controlador
    controller = MetodoPicoController(mongo)

    # Rutas
    @metodoPico_bp.route('/metodoPico', methods=['POST'])
    def crear_metodoPico():
        return controller.crear_metodoPico()

    @metodoPico_bp.route('/metodoPico', methods=['GET'])
    def obtener_metodosPico():
        return controller.obtener_metodosPico()

    @metodoPico_bp.route('/metodoPico/<id>', methods=['DELETE'])
    def eliminar_metodoPico(id):
        return controller.eliminar_metodoPico(id)
    

    return metodoPico_bp
