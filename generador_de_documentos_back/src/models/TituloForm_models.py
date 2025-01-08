from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError

class TituloFormModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.TituloForm = mongo.db.TituloForm
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'TituloForm_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def crear_tituloForm(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el diccionario de la investigación con el nuevo ID
            tituloForm = {
                'id': nuevo_id,
                'tema': data['tema']
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.TitulosForm.insert_one(tituloForm)
        except PyMongoError as e:
            raise e

    def obtener_titulosForm(self):
        try:
            titulosForm = list(self.mongo.db.TitulosForm.find())
            
            for tituloForm in titulosForm:
                tituloForm['id'] = str(tituloForm['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del tituloForm['_id']  # Opcional: eliminamos el campo original '_id'

            return titulosForm
        except PyMongoError as e:
            raise e
    
    def obtener_tituloForm_por_id(self, id):
        try:
            return self.mongo.db.TitulosForm.find_one({"id": id})
        except PyMongoError as e:
            raise e

    def obtener_ultimo_tituloForm(self):
        try:
            return self.mongo.db.TitulosForm.find().sort("id", -1).limit(1)[0]  # Obtiene el último título
        except PyMongoError as e:
            raise e
    
    def eliminar_tituloForm(self, id):
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.mongo.db.TitulosForm.delete_one({'id': id})
        except PyMongoError as e:
            raise e
