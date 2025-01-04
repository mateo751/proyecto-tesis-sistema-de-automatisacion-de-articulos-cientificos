from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError

class MetodoPicoFormModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.MetodosPico = mongo.db.MetodosPicoForm
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'MetodoPicoForm_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e

    def crear_metodoPicoForm(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()

            # Crear el diccionario de la investigación con el nuevo ID
            metodoPicoForm = {
                'id': nuevo_id,
                'pregunta_investigacion': data['pregunta_investigacion'],
                'sub_pregunta_1': data['sub_pregunta_1'],
                'sub_pregunta_2': data['sub_pregunta_2'],
                'sub_pregunta_3': data['sub_pregunta_3'],
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.MetodosPicoForm.insert_one(metodoPicoForm)
        except PyMongoError as e:
            raise e

    def obtener_metodosPicoForm(self):
        try:
            metodosPicoForm = list(self.mongo.db.MetodosPicoForm.find())
            
            for metodoPicoForm in metodosPicoForm:
                metodoPicoForm['id'] = str(metodoPicoForm['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del metodoPicoForm['_id']  # Opcional: eliminamos el campo original '_id'

            return metodosPicoForm
        except PyMongoError as e:
            raise e
    
    def eliminar_metodoPicoForm(self, id):
        try:
            # Buscar y eliminar el documento que tenga el campo 'id' igual al número pasado
            return self.mongo.db.MetodosPicoForm.delete_one({'id': id})
        except PyMongoError as e:
            raise e
