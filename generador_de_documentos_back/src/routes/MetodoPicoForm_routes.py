from flask import Blueprint
from src.controllers.MetodoPicoForm_controller import MetodoPicoFormController

def crear_rutas_metodoPicoForm(mongo):
    # Crear el Blueprint de las rutas
    metodoPicoForm_bp = Blueprint('metodoPicoForm_bp', __name__)
    controller = MetodoPicoFormController(mongo)

    # Rutas
    @metodoPicoForm_bp.route('/create/metodoPicoForm', methods=['POST'])
    def crear_metodoPico():
        return controller.crear_metodoPicoForm()

    @metodoPicoForm_bp.route('/create/metodoPicoForm', methods=['GET'])
    def obtener_metodosPico():
        return controller.obtener_metodosPicoForm()

    @metodoPicoForm_bp.route('/create/metodoPicoForm/<id>', methods=['DELETE'])
    def eliminar_metodoPico(id):
        return controller.eliminar_metodoPicoForm(id)
    

    return metodoPicoForm_bp
