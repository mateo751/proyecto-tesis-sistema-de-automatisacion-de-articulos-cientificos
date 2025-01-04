from flask import jsonify, request
import logging
from pymongo.errors import PyMongoError
from src.models.TituloForm_models import TituloFormModel
from src.service.MetodoPicoForm_service import OpenAIService

class TituloFormController:
    def __init__(self, mongo):
        self.model = TituloFormModel(mongo)
        self.ai_service = OpenAIService()

    def _log_error(self, error):
        logging.error(f"Error en el controlador: {str(error)}")

    def crear_tituloForm(self):
        try:
            data = request.get_json()
            if not data or 'tema' not in data:
                return jsonify({"error": "Falta el campo 'tema'."}), 400
            
            # Llamada al servicio para obtener PICO usando el tema y otros campos
            picoForm_response = self.ai_service.generar_metodo_pico_Form(
                tema=data.get('tema'),
                pregunta_investigacion=data.get('pregunta_investigacion', ''),
                sub_pregunta_1=data.get('sub_pregunta_1', ''),
                sub_pregunta_2=data.get('sub_pregunta_2', ''),
                sub_pregunta_3=data.get('sub_pregunta_3', '')
            )

            resultado = self.model.crear_tituloForm(data)
            return jsonify({"mensaje": "Título creado con éxito",
                            "pico_response": picoForm_response or "Sin respuesta PICO",
                            "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            self._log_error(e)
            return jsonify({"error": "Error al crear el título"}), 500
        except Exception as e:
            self._log_error(e)
            return jsonify({"error": "Error en la solicitud"}), 500

    def obtener_titulosForm(self):
        try:
            titulos_form = self.model.obtener_titulosForm()
            return jsonify(titulos_form), 200
        except PyMongoError as e:
            self._log_error(e)
            return jsonify({"error": "Error al obtener los títulos"}), 500

    def eliminar_tituloForm(self, id):
        try:
            id_numero = int(id)
            resultado = self.model.eliminar_tituloForm(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Título no encontrado"}), 404

            return jsonify({"mensaje": "Título eliminado con éxito"}), 200
        except ValueError:
            return jsonify({"error": "ID debe ser un número válido"}), 400
        except PyMongoError as e:
            self._log_error(e)
            return jsonify({"error": "Error al eliminar el título"}), 500
        except Exception as e:
            self._log_error(e)
            return jsonify({"error": "Error en la solicitud"}), 500
    
    