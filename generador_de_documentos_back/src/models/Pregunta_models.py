from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError

class PreguntaModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.Pregunta = mongo.db.Pregunta
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'Pregunta_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def crear_pregunta(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el diccionario de la investigación con el nuevo ID
            pregunta = {
                'id': nuevo_id,
                'programa_de_estudio': data['programa_de_estudio'],
                'enfoque_general': data['enfoque_general'],
                'identificar_problema': data['identificar_problema'],
                'idioma': data['idioma'],
                'pregunta_response': data['pregunta_response']
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.Preguntas.insert_one(pregunta)
        except PyMongoError as e:
            raise e

    def obtener_preguntas(self):
        try:
            preguntas = list(self.mongo.db.Preguntas.find())
            
            for pregunta in preguntas:
                pregunta['id'] = str(pregunta['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del pregunta['_id']  # Opcional: eliminamos el campo original '_id'

            return preguntas
        except PyMongoError as e:
            raise e
    
    def eliminar_pregunta(self, id):
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.mongo.db.Preguntas.delete_one({'id': id})
        except PyMongoError as e:
            raise e
