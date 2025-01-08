from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.routes.Investigaciones_routes import crear_rutas_investigaciones
from src.routes.InvestigacionForm_routes import crear_rutas_investigacionesForm

def create_app():
    app = Flask(__name__)

    # Habilitar CORS para toda la aplicación
    CORS(app)
    
    # Configuración de la base de datos MongoDB
    app.config["MONGO_URI"] =  os.getenv("MONGO_URI", "mongodb://localhost:27017/pi_database")
    
    # Inicializar MongoDB
    mongo = PyMongo(app)

    load_dotenv()  # Carga las variables del archivo .env
    
    app.register_blueprint(crear_rutas_investigaciones(mongo))
    app.register_blueprint(crear_rutas_investigacionesForm(mongo))
    

    
    return app