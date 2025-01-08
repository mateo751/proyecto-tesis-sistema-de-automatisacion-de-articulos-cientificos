from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.models.Pregunta_models import PreguntaModel
from src.service.Pregunta_service import OpenAIService

class PreguntaController:
    def __init__(self, mongo):
        self.model = PreguntaModel(mongo)
        self.openai_service = OpenAIService()
    def crear_Pregunta(self):
        try:
            data = request.get_json()
            # Validación de datos
            if not data or not all(key in data for key in ('programa_de_estudio', 'enfoque_general', 'identificar_problema', 'idioma')):
                return jsonify({"error": "Faltan datos obligatorios"}), 400
            # Obtener las variables
            programa_de_estudio = data['programa_de_estudio']
            enfoque_general = data['enfoque_general']
            identificar_problema = data['identificar_problema']
            idioma = data['idioma']
            
            # Generar preguntas con OpenAI
            pregunta_response = self.openai_service.generar_preguntas(
                programa_de_estudio,
                enfoque_general,
                identificar_problema,
                idioma
            )
            # Guardar el resultado en la base de datos
            data['pregunta_response'] = pregunta_response  # Añadir la respuesta PICO al objeto de datos
            resultado = self.model.crear_pregunta(data)
            
            return jsonify({"mensaje": "pregunta fue creada con éxito", 
                            "pregunta_response": pregunta_response or "Sin respuesta titulo",
                            "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al crear la pregunta", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_preguntas(self):
        try:
            preguntas = self.model.obtener_preguntas()
            return jsonify(preguntas), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener las preguntas", "detalles": str(e)}), 500
    
    def eliminar_pregunta(self, id):
        try:
            # Convertir el ID a un número entero, ya que 'id' es numérico, no ObjectId
            try:
                id_numero = int(id)  # Convertimos el id de string a número entero
            except ValueError:
                return jsonify({"error": "ID debe ser un número válido"}), 400

            # Llamamos al modelo para eliminar el documento con el campo 'id' igual al número
            resultado = self.model.eliminar_pregunta(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Preguntas no encontrado"}), 404

            return jsonify({"mensaje": "Preguntas eliminado con éxito"}), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al eliminar la preguntas", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

