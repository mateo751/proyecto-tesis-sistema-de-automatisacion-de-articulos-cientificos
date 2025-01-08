from typing import Dict, Any, List
from pymongo import ReturnDocument
from bson import ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime

class InvestigacionFormModel:
    """
    Modelo para manejar las operaciones de base de datos de los formularios de investigación
    """
    
    def __init__(self, mongo):
        """
        Inicializa el modelo con la conexión a MongoDB
        """
        self.mongo = mongo
        self.collection = mongo.db.InvestigacionForm
        self.counters = mongo.db.counters

    def obtener_siguiente_id(self) -> int:
        """
        Obtiene el siguiente ID disponible
        """
        try:
            contador = self.counters.find_one_and_update(
                {'id': 'InvestigacionForm_id'},
                {'$inc': {'seq': 1}},
                return_document=ReturnDocument.AFTER,
                upsert=True
            )
            return int(contador['seq'])
        except PyMongoError as e:
            raise e

    def crear_formulario_investigacion(self, data: Dict[str, Any]) -> int:
        #Crea un nuevo formulario de investigación
        try:
            # Obtener nuevo ID
            nuevo_id = self.obtener_siguiente_id()

            # Preparar documento
            investigacionForm = {
                'id': nuevo_id,
                'tema': data['tema'],
                'pregunta_investigacion': data['pregunta_investigacion'],
                'sub_pregunta_1': data['sub_pregunta_1'],
                'sub_pregunta_2': data['sub_pregunta_2'],
                'sub_pregunta_3': data['sub_pregunta_3'],
                'anio_inicio': data['anio_inicio'],
                'anio_fin': data['anio_fin'],
                'query': data['query'],
                'respuesta_fuentes': data.get('respuesta_fuentes'),
                'mapping_document': None,
                'generated_at': None,
                'created_at': datetime.utcnow(),
                'terminos_pico': data.get('terminos_pico', []),  # Agregar campo para términos PICO
                'cadenas_busqueda': data.get('cadenas_busqueda', [])            
            }

            # Insertar documento
            self.collection.insert_one(investigacionForm)
            return nuevo_id
            
        except PyMongoError as e:
            raise e

    def obtener_formularios_investigacion(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los formularios de investigación
        """
        try:
            investigaciones = list(self.collection.find())
            for investigacion in investigaciones:
                investigacion['_id'] = str(investigacion['_id'])
            return investigaciones
        except PyMongoError as e:
            raise e

    def obtener_formulario_investigacion_por_id(self, id: int) -> Dict[str, Any]:
        """
        Obtiene una investigación por su ID
        """
        try:
            return self.collection.find_one({'id': id})
        except PyMongoError as e:
            raise e

    def actualizar_formulario_investigacion(self, id: int, data: Dict[str, Any]):
        """
        Actualiza un formulario de investigación
        """
        try:
            data['updated_at'] = datetime.utcnow()
            return self.collection.update_one(
                {'id': id},
                {'$set': data}
            )
        except PyMongoError as e:
            raise e

    def actualizar_documento_mapeo(self, id: int, documento: str, fecha_generacion: datetime):
        """
        Actualiza el documento de mapeo sistemático
        """
        try:
            return self.collection.update_one(
                {'id': id},
                {
                    '$set': {
                        'mapping_document': documento,
                        'generated_at': fecha_generacion
                    }
                }
            )
        except PyMongoError as e:
            raise e

    def eliminar_formulario_investigacion(self, id: int):
        """
        Elimina un formulario de investigación
        """
        try:
            return self.collection.delete_one({'id': id})
        except PyMongoError as e:
            raise e