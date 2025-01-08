from pymongo import ReturnDocument
from datetime import datetime
from pymongo.errors import PyMongoError

class InvestigacionModel:
    def __init__(self, mongo):
        self.mongo = mongo
        self.MetodosPico = mongo.db.MetodosPico
        self.counters = mongo.db.counters  # Colección para el contador de IDs
    
    
    def obtener_siguiente_id(self):
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'Investigacion_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True  # Si no existe, lo crea con valor inicial
            )
            return contador['seq']
        except PyMongoError as e:
            raise e
    
    # Crear nueva investigación
    def crear_investigacion(self, data):
        try:
            # Obtén el nuevo ID auto incremental
            nuevo_id = self.obtener_siguiente_id()
            # Añadimos la fecha actual al diccionario de datos
            fecha_actual = datetime.now()

            # Crear el diccionario de la investigación con el nuevo ID
            investigacion = {
                'id': nuevo_id,
                'nombre': data['nombre'],
                'tipo': data['tipo'],
                'fecha': fecha_actual
            }

            # Insertar la investigación en la base de datos
            return self.mongo.db.Investigaciones.insert_one(investigacion)
        except PyMongoError as e:
            raise e

    # Obtener todas las investigaciones
    def obtener_investigaciones(self):
        try:
            investigaciones = list(self.mongo.db.Investigaciones.find())
            
            for investigacion in investigaciones:
                investigacion['id'] = str(investigacion['_id'])  # Convertimos el ObjectId a string y lo asignamos a 'id'
                del investigacion['_id']  # Opcional: eliminamos el campo original '_id'

            return investigaciones
        except PyMongoError as e:
            raise e

    # Eliminar investigación por ID
    def eliminar_investigacion(self, id):
        try:
            # Convertir ID a ObjectId de MongoDB
            return self.mongo.db.Investigaciones.delete_one({'id': id})
        except PyMongoError as e:
            raise e
