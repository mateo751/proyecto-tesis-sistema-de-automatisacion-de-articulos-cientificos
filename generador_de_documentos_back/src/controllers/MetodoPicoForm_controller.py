from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.models.MetodoPicoForm_models import MetodoPicoFormModel


class MetodoPicoFormController:
    def __init__(self, mongo):
        self.model = MetodoPicoFormModel(mongo)

    def crear_metodoPicoForm(self):
        try:
            data = request.get_json()
            # Validación de datos
            if not data or not all(key in data for key in ('pregunta_investigacion', 'sub_pregunta_1', 'sub_pregunta_2', 'sub_pregunta_3')):
                return jsonify({"error": "Faltan datos obligatorios"}), 400
            # Obtener las variables
            pregunta_investigacion = data['pregunta_investigacion']
            sub_pregunta_1 = data['sub_pregunta_1']
            sub_pregunta_2 = data['sub_pregunta_2']
            sub_pregunta_3 = data['sub_pregunta_3']
            
            resultado = self.model.crear_metodoPicoForm(data)
            
            return jsonify({"mensaje": "Metodo Pico creada con éxito", 
                            "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al crear el metodo pico", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_metodosPicoForm(self):
        try:
            metodosPicoForm = self.model.obtener_metodosPicoForm()
            return jsonify(metodosPicoForm), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener los metodos Pico", "detalles": str(e)}), 500
    
    def eliminar_metodoPicoForm(self, id):
        try:
            # Convertir el ID a un número entero, ya que 'id' es numérico, no ObjectId
            try:
                id_numero = int(id)  # Convertimos el id de string a número entero
            except ValueError:
                return jsonify({"error": "ID debe ser un número válido"}), 400

            # Llamamos al modelo para eliminar el documento con el campo 'id' igual al número
            resultado = self.model.eliminar_metodoPicoForm(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Metodo no encontrado"}), 404

            return jsonify({"mensaje": "Metodo eliminado con éxito"}), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al eliminar el metodo", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500
