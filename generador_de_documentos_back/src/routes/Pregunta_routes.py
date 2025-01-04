from flask import Blueprint
from src.controllers.Pregunta_controller import PreguntaController

def crear_rutas_pregunta(mongo):
    # Crear el Blueprint de las rutas
    pregunta_bp = Blueprint('pregunta_bp', __name__)
    
    # Crear una instancia del controlador
    controller = PreguntaController(mongo)

    # Rutas
    @pregunta_bp.route('/preguntas', methods=['POST'])
    def crear_pregunta():
        return controller.crear_Pregunta()

    @pregunta_bp.route('/preguntas', methods=['GET'])
    def obtener_pregunta():
        return controller.obtener_preguntas()

    @pregunta_bp.route('/preguntas/<id>', methods=['DELETE'])
    def eliminar_pregunta(id):
        return controller.eliminar_pregunta(id)
    

    return pregunta_bp
