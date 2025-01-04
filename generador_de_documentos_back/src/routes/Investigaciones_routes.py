from flask import Blueprint
from src.controllers.Investigacion_controller import InvestigacionController

def crear_rutas_investigaciones(mongo):
    # Crear el Blueprint de las rutas
    investigacion_bp = Blueprint('investigacion_bp', __name__)
    
    # Crear una instancia del controlador
    controller = InvestigacionController(mongo)

    # Rutas
    @investigacion_bp.route('/investigaciones', methods=['POST'])
    def crear_investigacion():
        return controller.crear_investigacion()

    @investigacion_bp.route('/investigaciones', methods=['GET'])
    def obtener_investigaciones():
        return controller.obtener_investigaciones()

    @investigacion_bp.route('/investigaciones/<id>', methods=['DELETE'])
    def eliminar_investigacion(id):
        return controller.eliminar_investigacion(id)
    

    return investigacion_bp
