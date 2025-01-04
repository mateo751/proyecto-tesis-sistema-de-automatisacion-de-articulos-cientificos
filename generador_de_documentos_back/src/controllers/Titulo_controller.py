from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.models.Titulo_models import TituloModel
from src.service.Titulo_service import OpenAIService

class TituloController:
    def __init__(self, mongo):
        self.model = TituloModel(mongo)
        self.openai_service = OpenAIService()
    def crear_titulo(self):
        try:
            data = request.get_json()
            # Validación de datos
            if not data or not all(key in data for key in ('programa_de_estudio', 'asignatura', 'intereses', 'idioma')):
                return jsonify({"error": "Faltan datos obligatorios"}), 400
            # Obtener las variables
            programa_de_estudio = data['programa_de_estudio']
            asignatura = data['asignatura']
            intereses = data['intereses']
            idioma = data['idioma']
            
            # Generar el método PICO con OpenAI
            titulo_response = self.openai_service.generar_titulo(
                programa_de_estudio,
                asignatura,
                intereses,
                idioma
            )
            # Guardar el resultado en la base de datos
            data['titulo_response'] = titulo_response  # Añadir la respuesta PICO al objeto de datos
            resultado = self.model.crear_titulo(data)
            
            return jsonify({"mensaje": "Titulo creada con éxito", 
                            "titulo_response": titulo_response or "Sin respuesta titulo",
                            "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al crear el titulo", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_titulos(self):
        try:
            titulos = self.model.obtener_titulos()
            return jsonify(titulos), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener los titulos", "detalles": str(e)}), 500
    
    def eliminar_titulo(self, id):
        try:
            # Convertir el ID a un número entero, ya que 'id' es numérico, no ObjectId
            try:
                id_numero = int(id)  # Convertimos el id de string a número entero
            except ValueError:
                return jsonify({"error": "ID debe ser un número válido"}), 400

            # Llamamos al modelo para eliminar el documento con el campo 'id' igual al número
            resultado = self.model.eliminar_titulo(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Titulo no encontrado"}), 404

            return jsonify({"mensaje": "Titulo eliminado con éxito"}), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al eliminar el titulo", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

