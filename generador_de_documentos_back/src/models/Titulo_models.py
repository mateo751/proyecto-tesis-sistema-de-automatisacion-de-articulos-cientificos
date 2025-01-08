from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError

class TituloModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.Titulo = mongo.db.Titulo
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'Titulo_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def crear_titulo(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el diccionario de la investigación con el nuevo ID
            titulo = {
                'id': nuevo_id,
                'programa_de_estudio': data['programa_de_estudio'],
                'asignatura': data['asignatura'],
                'intereses': data['intereses'],
                'idioma': data['idioma'],
                'titulo_response': data['titulo_response']
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.Titulos.insert_one(titulo)
        except PyMongoError as e:
            raise e

    def obtener_titulos(self):
        try:
            titulos = list(self.mongo.db.Titulos.find())
            
            for titulo in titulos:
                titulo['id'] = str(titulo['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del titulo['_id']  # Opcional: eliminamos el campo original '_id'

            return titulos
        except PyMongoError as e:
            raise e
    
    def eliminar_titulo(self, id):
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.mongo.db.Titulos.delete_one({'id': id})
        except PyMongoError as e:
            raise e
