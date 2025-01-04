from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError

class MetodoPicoModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.MetodosPico = mongo.db.MetodosPico
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'MetodoPico_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def crear_metodoPico(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el diccionario de la investigación con el nuevo ID
            metodoPico = {
                'id': nuevo_id,
                'tema': data['tema'],
                'pregunta_investigacion': data['pregunta_investigacion'],
                'sub_pregunta_1': data['sub_pregunta_1'],
                'sub_pregunta_2': data['sub_pregunta_2'],
                'sub_pregunta_3': data['sub_pregunta_3'],
                'pico_response': data['pico_response']
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.MetodosPico.insert_one(metodoPico)
        except PyMongoError as e:
            raise e

    def obtener_metodosPico(self):
        try:
            metodosPico = list(self.mongo.db.MetodosPico.find())
            
            for metodoPico in metodosPico:
                metodoPico['id'] = str(metodoPico['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del metodoPico['_id']  # Opcional: eliminamos el campo original '_id'

            return metodosPico
        except PyMongoError as e:
            raise e
    
    def eliminar_metodoPico(self, id):
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.mongo.db.MetodosPico.delete_one({'id': id})
        except PyMongoError as e:
            raise e
