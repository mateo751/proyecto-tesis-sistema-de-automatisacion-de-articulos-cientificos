from bson import ObjectId
from flask import jsonify, request
from src.models.Investigacion_models import InvestigacionModel
from pymongo.errors import PyMongoError

class InvestigacionController:
    def __init__(self, mongo):
        self.model = InvestigacionModel(mongo)
    
    def crear_investigacion(self):
        try:
            data = request.get_json()

            # Validación de datos
            if not data or not all(key in data for key in ('nombre', 'tipo')):
                return jsonify({"error": "Faltan datos obligatorios"}), 400

            resultado = self.model.crear_investigacion(data)
            return jsonify({"mensaje": "Investigación creada con éxito", "id": str(resultado.inserted_id)}), 201
        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al crear la investigación", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_investigaciones(self):
        try:
            investigaciones = self.model.obtener_investigaciones()
            return jsonify(investigaciones), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener las investigaciones", "detalles": str(e)}), 500
    
    def eliminar_investigacion(self, id):
        try:
            # Convertir el ID a un número entero, ya que 'id' es numérico, no ObjectId
            try:
                id_numero = int(id)  # Convertimos el id de string a número entero
            except ValueError:
                return jsonify({"error": "ID debe ser un número válido"}), 400

            resultado = self.model.eliminar_investigacion(id_numero)

            if resultado.deleted_count == 0:
                return jsonify({"error": "Investigación no encontrada"}), 404

            return jsonify({"mensaje": "Investigación eliminada con éxito"}), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al eliminar la investigación", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500
