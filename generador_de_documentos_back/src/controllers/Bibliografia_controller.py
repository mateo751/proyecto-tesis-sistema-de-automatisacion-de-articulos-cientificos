from flask import jsonify, request
from pymongo.errors import PyMongoError
from src.service.Bibliografia_service import ScopusService
from src.models.Bibliografia_models import ScopusModel

class ScopusController:
    def __init__(self, mongo):
        self.scopus_service = ScopusService()
        self.model = ScopusModel(mongo)

    def buscar_en_scopus(self):
        try:
            data = request.get_json()
            # Validación de datos
            if not data or 'query' not in data:
                return jsonify({"error": "El campo 'query' es obligatorio"}), 400

            # Obtener los parámetros de búsqueda
            query = data['query']
            count = data.get('count', 10)  # Valor predeterminado: 10
            start = data.get('start', 0)  # Inicio para paginación (default: 0)

            # Llamar al servicio de Scopus para buscar artículos
            resultados = self.scopus_service.buscar(query, count, start)

            if "error" in resultados:
                return jsonify({"error": resultados['error'], "detalles": resultados.get('details', '')}), 500

            # Guardar los resultados en la base de datos
            self.model.guardar_busqueda(query, resultados)

            return jsonify({
                "mensaje": "Búsqueda en Scopus realizada con éxito",
                "resultados": resultados
            }), 200

        except PyMongoError as e:
            # Manejo de errores relacionados con MongoDB
            return jsonify({"error": "Error al guardar los resultados en la base de datos", "detalles": str(e)}), 500
        except Exception as e:
            # Manejo de errores generales
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500

    def obtener_busquedas_scopus(self):
        try:
            # Obtener las búsquedas guardadas en la base de datos
            busquedas = self.model.obtener_busquedas()
            return jsonify(busquedas), 200
        except PyMongoError as e:
            return jsonify({"error": "Error al obtener las búsquedas de Scopus", "detalles": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Error en la solicitud", "detalles": str(e)}), 500
