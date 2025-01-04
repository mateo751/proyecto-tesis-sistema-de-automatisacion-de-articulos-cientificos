from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.models.MetodoPico_models import MetodoPicoModel
from src.service.MetodoPico_service import OpenAIService

class MetodoPicoController:
    def __init__(self, mongo):
        self.model = MetodoPicoModel(mongo)
        self.openai_service = OpenAIService()
    def crear_metodoPico(self):
        try:
            data = request.get_json()
            # Validación de datos
            if not data or not all(key in data for key in ('tema', 'pregunta_investigacion', 'sub_pregunta_1', 'sub_pregunta_2', 'sub_pregunta_3')):
                return jsonify({"error": "Faltan datos obligatorios"}), 400
            # Obtener las variables
            tema = data['tema']
            pregunta_investigacion = data['pregunta_investigacion']
            sub_pregunta_1 = data['sub_pregunta_1']
            sub_pregunta_2 = data['sub_pregunta_2']
            sub_pregunta_3 = data['sub_pregunta_3']
            
            # Generar el método PICO con OpenAI
            pico_response = self.openai_service.generar_metodo_pico(
                tema,
                pregunta_investigacion,
                sub_pregunta_1,
                sub_pregunta_2,
                sub_pregunta_3
            )
            # Guardar el resultado en la base de datos
            data['pico_response'] = pico_response  # Añadir la respuesta PICO al objeto de datos
            resultado = self.model.crear_metodoPico(data)
            
            return jsonify({"mensaje": "Metodo Pico creada con éxito", 
                            "pico_response": pico_response or "Sin respuesta PICO",
                            "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al crear el metodo pico", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_metodosPico(self):
        try:
            metodosPico = self.model.obtener_metodosPico()
            return jsonify(metodosPico), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener los metodos Pico", "detalles": str(e)}), 500
    
    def eliminar_metodoPico(self, id):
        try:
            # Convertir el ID a un número entero, ya que 'id' es numérico, no ObjectId
            try:
                id_numero = int(id)  # Convertimos el id de string a número entero
            except ValueError:
                return jsonify({"error": "ID debe ser un número válido"}), 400

            # Llamamos al modelo para eliminar el documento con el campo 'id' igual al número
            resultado = self.model.eliminar_metodoPico(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Metodo no encontrado"}), 404

            return jsonify({"mensaje": "Metodo eliminado con éxito"}), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al eliminar el metodo", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

