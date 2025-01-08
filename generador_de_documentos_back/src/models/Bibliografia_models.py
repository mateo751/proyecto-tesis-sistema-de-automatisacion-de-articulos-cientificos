from pymongo.errors import PyMongoError
from pymongo import ReturnDocument

class ScopusModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.scopus_results = mongo.db.ScopusResults  # Colección para guardar los resultados de búsquedas
        self.counters = mongo.db.counters  # Colección para el contador de IDs

    def obtener_siguiente_id(self):
        """
        Obtiene el siguiente ID auto incremental para las búsquedas de Scopus.
        """
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'ScopusResults_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe el documento, lo crea con un valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def guardar_busqueda(self, query, resultados):
        """
        Guarda una búsqueda de Scopus junto con sus resultados en la base de datos.
        """
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el documento para almacenar
            busqueda = {
                'id': nuevo_id,
                'query': query,
                'resultados': resultados
            }

            # Insertar en la base de datos
            return self.scopus_results.insert_one(busqueda)
        except PyMongoError as e:
            raise e

    def obtener_busquedas(self):
        """
        Obtiene todas las búsquedas de Scopus almacenadas en la base de datos.
        """
        try:
            busquedas = list(self.scopus_results.find())

            for busqueda in busquedas:
                busqueda['id'] = str(busqueda['_id'])  # Convertimos el ObjectId a string para 'id'
                del busqueda['_id']  # Opcional: eliminamos el campo '_id' original

            return busquedas
        except PyMongoError as e:
            raise e

    def eliminar_busqueda(self, id):
        """
        Elimina una búsqueda de Scopus por su ID.
        """
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.scopus_results.delete_one({'id': id})
        except PyMongoError as e:
            raise e
