from flask import Flask
from flask_pymongo import PyMongo
from src.routes.Investigaciones_routes import crear_rutas_investigaciones
from src.routes.MetodoPico_routes import crear_rutas_metodoPico
from src.routes.Titulo_routes import crear_rutas_titulo
from src.routes.TituloForm_routes import crear_rutas_tituloForm
from src.routes.Pregunta_routes import crear_rutas_pregunta
from src.routes.MetodoPicoForm_routes import crear_rutas_metodoPicoForm
from src.routes.InvestigacionForm_routes import crear_rutas_investigacionesForm
from src.routes.Bibliografia_routes import crear_rutas_scopus

from flask_cors import CORS
from dotenv import load_dotenv
import os

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
    app.register_blueprint(crear_rutas_metodoPico(mongo))
    app.register_blueprint(crear_rutas_titulo(mongo))
    app.register_blueprint(crear_rutas_tituloForm(mongo))
    app.register_blueprint(crear_rutas_metodoPicoForm(mongo))
    app.register_blueprint(crear_rutas_pregunta(mongo))
    app.register_blueprint(crear_rutas_investigacionesForm(mongo))
    app.register_blueprint(crear_rutas_scopus(mongo))
    
    return app