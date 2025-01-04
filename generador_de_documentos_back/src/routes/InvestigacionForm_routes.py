from flask import Blueprint
from src.controllers.InvestigacionForm_controller import InvestigacionFormController

def crear_rutas_investigacionesForm(mongo):
    # Crear el Blueprint de las rutas
    investigacionesForm_bp = Blueprint('investigacionesForm_bp', __name__)
    
    # Crear una instancia del controlador
    controller = InvestigacionFormController(mongo)

    # Rutas
    @investigacionesForm_bp.route('/Investigaciones/create', methods=['POST'])
    def crear_investigacionesForm():
        return controller.crear_investigacionForm()

    @investigacionesForm_bp.route('/Investigaciones/create', methods=['GET'])
    def obtener_investigacionesForm():
        return controller.obtener_investigacionesForm()
    
    @investigacionesForm_bp.route('/Investigaciones/create/<id>', methods=['DELETE'])
    def eliminar_investigacionesForm(id):
        return controller.eliminar_investigacionForm(id)

    return investigacionesForm_bp
