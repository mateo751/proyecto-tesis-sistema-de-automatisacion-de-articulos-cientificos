from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos MongoDB
    app.config["MONGO_URI"] = "mongodb://localhost:27017/pi_database"
    
    # Inicialización de MongoDB
    mongo = PyMongo(app)
    
    return app, mongo