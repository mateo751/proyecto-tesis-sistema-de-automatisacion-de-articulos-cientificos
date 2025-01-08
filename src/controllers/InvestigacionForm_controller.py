from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.models.InvestigacionForm_models import InvestigacionFormModel
from src.service.Bibliografia_service import ScopusService as ServicioScopus
from src.utils.ExtracionPico_utils import extraer_terminos_pico
from src.utils.GeneradorCadenaBusqueda_utils import generar_cadenas_busqueda
class ControladorFormularioInvestigacion:
    def __init__(self, mongo):
        self.modelo = InvestigacionFormModel(mongo)
        self.servicio_scopus = ServicioScopus()

    def crear_formulario_investigacion(self):
        try:
            datos = request.json
            campos_requeridos = ['tema', 'pregunta_investigacion', 'sub_pregunta_1', 
                                 'sub_pregunta_2', 'sub_pregunta_3', 'anio_inicio', 
                                 'anio_fin', 'query']
            for campo in campos_requeridos:
                if campo not in datos:
                    return jsonify({"error": f"Campo requerido faltante: {campo}"}), 400
                
            # Extraer términos PICO de la pregunta de investigación
            tema_investigacion = datos['tema']
            terminos_pico = extraer_terminos_pico(tema_investigacion)
            datos['terminos_pico'] = terminos_pico
            
            # Generar cadenas de búsqueda
            cadenas_busqueda = generar_cadenas_busqueda(terminos_pico, min_terminos=4, max_terminos=5)
            datos['cadenas_busqueda'] = cadenas_busqueda
            
            try:
                datos['respuesta_fuentes'] = self.servicio_scopus.generar_respuesta_fuentes(datos)  
            except Exception as e:
                print(f"Error generando respuesta de fuentes: {str(e)}")
                datos['respuesta_fuentes'] = None

            nuevo_id = self.modelo.crear_formulario_investigacion(datos)
            
            try:
                resultado_mapeo = self.servicio_mapeo_sistematico.generar_documento_mapeo(nuevo_id)
            except Exception as e: 
                print(f"Error generando documento de mapeo: {str(e)}")
                resultado_mapeo = {'exito': False, 'error': str(e)}
            
            return jsonify({
                "mensaje": "Formulario de investigación creado exitosamente", 
                "id": str(nuevo_id),
                "respuesta_fuentes": datos['respuesta_fuentes'],
                "advertencia": "Se creó el formulario pero hubo errores generando documentos asociados" 
                               if not resultado_mapeo.get('exito') else None
            }), 201

        except PyMongoError as e:
            return jsonify({"error": "Error en la base de datos", "detalles": str(e)}), 500

    def obtener_formularios_investigacion(self):
        try:
            formularios = self.modelo.obtener_formularios_investigacion()
            return jsonify(formularios), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener los formularios", "detalles": str(e)}), 500

    def eliminar_formulario_investigacion(self, id):
        try:
            id_numero = int(id)
            resultado = self.modelo.eliminar_formulario_investigacion(id_numero)
            
            if resultado.deleted_count == 0:
                return jsonify({"error": "Formulario no encontrado"}), 404
            
            return jsonify({"mensaje": "Formulario eliminado con éxito"}), 200
        
        except ValueError:
            return jsonify({"error": "ID debe ser un número válido"}), 400
        except PyMongoError as e:
            return jsonify({"error": "Error en la base de datos", "detalles": str(e)}), 500

    def obtener_documento_mapeo(self, id):
        try:
            id_numero = int(id)
            resultado = self.servicio_mapeo_sistematico.obtener_documento(id_numero)
            
            if resultado.get('exito'):
                return jsonify(resultado), 200
            else:
                return jsonify({"error": resultado.get('error', "Error al obtener el documento")}), 404
        
        except ValueError:
            return jsonify({"error": "ID inválido"}), 400        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def generar_documento_mapeo(self, id):
        try:
            id_numero = int(id)
            resultado = self.servicio_mapeo_sistematico.generar_documento_mapeo(id_numero)
            
            if resultado.get('exito'):
                return jsonify({
                    "mensaje": "Documento generado exitosamente",
                    "documento": resultado.get('documento'),
                    "estadisticas": resultado.get('estadisticas')
                }), 200
            else:
                return jsonify({"error": resultado.get('error', "Error al generar el documento")}), 400
        
        except ValueError:
            return jsonify({"error": "ID inválido"}), 400
        except Exception as e:  
            return jsonify({"error": str(e)}), 500