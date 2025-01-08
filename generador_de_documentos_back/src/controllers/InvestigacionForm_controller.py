from flask import jsonify, request
from pymongo.errors import PyMongoError
from typing import Dict, Any, Optional
from datetime import datetime

from src.models.InvestigacionForm_models import InvestigacionFormModel
from src.service.Bibliografia_service import ScopusService
from src.service.GenerarDocumento_service import GenerarMetodosMaterialesService
from src.service.InvestigacionForm_service import OpenAIService

class InvestigacionFormController:
    """
    Controlador para gestionar las operaciones de los formularios de investigación
    """

    def __init__(self, mongo):
        """
        Inicializa el controlador con sus dependencias
        """
        self.model = InvestigacionFormModel(mongo)
        self.openai_service = OpenAIService()
        self.scopus_service = ScopusService()
        self.systematic_mapping_service = GenerarMetodosMaterialesService(mongo)

    def crear_investigacionForm(self):
        """
        Crea una nueva investigación y genera documentos asociados
        """
        try:
            data = request.json
            
            # Validar datos requeridos
            required_fields = ['tema', 'pregunta_investigacion', 'sub_pregunta_1', 
                             'sub_pregunta_2', 'sub_pregunta_3', 'anio_inicio', 
                             'anio_fin', 'query']
            
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Campo requerido faltante: {field}"}), 400

            # Generar respuesta PICO
            try:
                pico_response = self.openai_service.generar_metodo_pico(data['tema'])
                data['pico_response'] = pico_response
            except Exception as e:
                print(f"Error generando respuesta PICO: {str(e)}")
                data['pico_response'] = None

            # Generar respuesta de fuentes
            try:
                fuentes_response = self.scopus_service.generar_respuesta_fuentes(data)
                data['fuentes_response'] = fuentes_response
            except Exception as e:
                print(f"Error generando respuesta de fuentes: {str(e)}")
                data['fuentes_response'] = None

            # Crear la investigación y obtener el ID numérico
            nuevo_id = self.model.crear_investigacionForm(data)
            
            # Generar documento de mapeo usando el ID numérico
            try:
                mapping_result = self.systematic_mapping_service.generate_mapping_document(nuevo_id)
            except Exception as e:
                print(f"Error generando documento de mapeo: {str(e)}")
                mapping_result = {'success': False, 'error': str(e)}

            return jsonify({
                "mensaje": "Investigación creada exitosamente",
                "id": str(nuevo_id),
                "pico_response": pico_response,
                "fuentes_response": fuentes_response,
                "warning": "Se creó la investigación pero hubo errores generando documentos asociados" 
                          if not mapping_result.get('success') else None
            }), 201

        except PyMongoError as e:
            return jsonify({
                "error": "Error en la base de datos",
                "detalles": str(e)
            }), 500
        except Exception as e:
            return jsonify({
                "error": "Error en la solicitud",
                "detalles": str(e)
            }), 500

    def obtener_investigacionesForm(self):
        """
        Obtiene todos los formularios de investigación
        """
        try:
            investigaciones = self.model.obtener_investigacionForm()
            return jsonify(investigaciones), 200
        except PyMongoError as e:
            return jsonify({
                "error": "Error al obtener las investigaciones",
                "detalles": str(e)
            }), 500

    def eliminar_investigacionForm(self, id: str):
        """
        Elimina un formulario de investigación
        """
        try:
            # Validar y convertir ID
            try:
                id_numero = int(id)
            except ValueError:
                return jsonify({
                    "error": "ID debe ser un número válido"
                }), 400

            resultado = self.model.eliminar_investigacionForm(id_numero)
            
            if resultado.deleted_count == 0:
                return jsonify({
                    "error": "Investigación no encontrada"
                }), 404

            return jsonify({
                "mensaje": "Investigación eliminada con éxito"
            }), 200

        except PyMongoError as e:
            return jsonify({
                "error": "Error en la base de datos",
                "detalles": str(e)
            }), 500
        except Exception as e:
            return jsonify({
                "error": "Error en la solicitud",
                "detalles": str(e)
            }), 500

    def obtener_mapping_document(self, id: str):
        """
        Obtiene el documento de mapeo sistemático
        """
        try:
            id_numero = int(id)
            result = self.systematic_mapping_service.get_document(id_numero)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({
                    "error": result.get('error', "Error al obtener el documento")
                }), 404
                
        except ValueError:
            return jsonify({
                "error": "ID inválido"
            }), 400
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def generar_mapping_document(self, id: str):
        """
        Genera o regenera el documento de mapeo sistemático
        """
        try:
            id_numero = int(id)
            result = self.systematic_mapping_service.generate_mapping_document(id_numero)
            
            if result.get('success'):
                return jsonify({
                    "mensaje": "Documento generado exitosamente",
                    "document": result.get('document'),
                    "statistics": result.get('statistics')
                }), 200
            else:
                return jsonify({
                    "error": result.get('error', "Error al generar el documento")
                }), 400
                
        except ValueError:
            return jsonify({
                "error": "ID inválido"
            }), 400
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500