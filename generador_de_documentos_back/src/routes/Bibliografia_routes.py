from flask import Blueprint
from src.controllers.Bibliografia_controller import ScopusController

def crear_rutas_scopus(mongo):
    # Crear el Blueprint para las rutas de Scopus
    scopus_bp = Blueprint('scopus_bp', __name__)
    
    # Crear una instancia del controlador
    controller = ScopusController(mongo)

    # Rutas
    @scopus_bp.route('/encontrar-fuentes', methods=['POST'])
    def buscar_en_scopus():
        return controller.buscar_en_scopus()

    @scopus_bp.route('/encontrar-fuentes', methods=['GET'])
    def obtener_busquedas_scopus():
        return controller.obtener_busquedas_scopus()

    @scopus_bp.route('/encontrar-fuentes/<id>', methods=['DELETE'])
    def eliminar_busqueda_scopus(id):
        return controller.eliminar_busqueda(id)
    
    return scopus_bp
