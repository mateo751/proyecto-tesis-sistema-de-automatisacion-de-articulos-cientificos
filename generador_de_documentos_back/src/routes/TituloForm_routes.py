from flask import Blueprint, request
from src.controllers.TituloForm_controller import TituloFormController

def crear_rutas_tituloForm(mongo):
    tituloForm_bp = Blueprint('titulo_form_bp', __name__)
    controller = TituloFormController(mongo)

    # Ruta para crear un nuevo título
    @tituloForm_bp.route('/create/tituloForm', methods=['POST'])
    def crear_titulo():
        return controller.crear_tituloForm()

    # Ruta para obtener todos los títulos
    @tituloForm_bp.route('/create/tituloForm', methods=['GET'])
    def obtener_titulos():
        return controller.obtener_titulosForm()

    # Ruta para eliminar un título por ID
    @tituloForm_bp.route('/create/tituloForm/<id>', methods=['DELETE'])
    def eliminar_titulo(id):
        return controller.eliminar_tituloForm(id)

    
    return tituloForm_bp
