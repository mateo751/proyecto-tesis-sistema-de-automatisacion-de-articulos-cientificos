from flask import Blueprint
from src.controllers.InvestigacionForm_controller import ControladorFormularioInvestigacion 

def crear_rutas_investigacionesForm(mongo):
    # Crear el Blueprint de las rutas
    investigacionesForm_bp = Blueprint('investigacionesForm_bp', __name__)
    
    # Crear una instancia del controlador
    controller = ControladorFormularioInvestigacion(mongo)

    # Rutas
    @investigacionesForm_bp.route('/Investigaciones/create', methods=['POST'])
    def crear_formulario_investigacion():
        return controller.crear_formulario_investigacion()

    @investigacionesForm_bp.route('/Investigaciones/create', methods=['GET'])
    def obtener_formularios_investigacion():
        return controller.obtener_formularios_investigacion()
    
    @investigacionesForm_bp.route('/Investigaciones/create/<id>', methods=['DELETE'])
    def eliminar_formulario_investigacion(id):
        return controller.eliminar_formulario_investigacion(id)

    return investigacionesForm_bp
