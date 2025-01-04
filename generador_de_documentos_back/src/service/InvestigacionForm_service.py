import openai
import os
import re
from flask import Flask, jsonify, request

app = Flask(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def parse_response(self, response_content):
        # Inicializa el diccionario para almacenar cada categoría
        categories = {
            "Poblacion": {},
            "Intervencion": {},
            "Resultado": {}
        }
        search_strings = {
            "Cadena_de_busqueda_1": "",
            "Cadena_de_busqueda_2": "",
            "Cadena_de_busqueda_3": ""
        }

        # Expresiones regulares para capturar las cadenas de búsqueda
        search_string_pattern = re.compile(r"Cadena de búsqueda (\d+):\s*(.+)")

        # Asegurarse de que response_content sea string
        if isinstance(response_content, dict):
            response_content = str(response_content)

        # Divide el contenido en líneas y utiliza un puntero para la categoría actual
        lines = response_content.split('\n')
        current_category = None
        term_index = 1

        # Recorre cada línea para clasificar los términos en las categorías correspondientes
        for line in lines:
            # Asegurarse de que line sea string antes de llamar strip()
            if not isinstance(line, str):
                continue
                
            line = line.strip()
            
            if not line:  # Ignorar líneas vacías
                continue

            # Detecta el inicio de cada categoría y resetea el índice de términos
            if "Población:" in line:
                current_category = "Poblacion"
                term_index = 1
            elif "Intervención:" in line:
                current_category = "Intervencion"
                term_index = 1
            elif "Resultado:" in line:
                current_category = "Resultado"
                term_index = 1
            elif "Cadenas de búsqueda:" in line:
                current_category = "Cadenas_de_busqueda"
                term_index = 1
            elif current_category == "Cadenas_de_busqueda":
                match = search_string_pattern.match(line)
                if match:
                    string_number = match.group(1)
                    search_string = match.group(2)
                    search_strings[f"Cadena_de_busqueda_{string_number}"] = search_string
            elif current_category and current_category != "Cadenas_de_busqueda":
                # Guarda cada sinónimo en la categoría actual si la línea no está vacía
                if line and not line.startswith('-'):
                    categories[current_category][f"Sinonimo_{term_index}"] = line
                    term_index += 1

        # Construimos el resultado final
        result = {
            "Intervencion": categories["Intervencion"],
            "Poblacion": categories["Poblacion"],
            "Resultado": categories["Resultado"],
            "Cadena_de_busqueda_1": search_strings["Cadena_de_busqueda_1"],
            "Cadena_de_busqueda_2": search_strings["Cadena_de_busqueda_2"],
            "Cadena_de_busqueda_3": search_strings["Cadena_de_busqueda_3"]
        }

        return result

    def generar_metodo_pico(self, tema):
        prompt = f"""
        Tengo el siguiente tema de investigación: "{tema}"

        Usando la estructura PICO (Población, Intervención, Resultado), genera palabras clave relevantes y específicas para un mapeo sistemático. Sigue el siguiente formato exacto:

        Población:
            [Una palabra clave relevante]
            [1 sinónimo relevante],
            [2 sinónimos relevantes]

        Intervención:
            [Una palabra clave relevante]
            [1 sinónimo relevante],
            [2 sinónimos relevantes]

        Resultado:
            [Una palabra clave relevante]
            [1 sinónimo relevante],
            [2 sinónimos relevantes]

        Cadenas de búsqueda:
            Cadena de búsqueda 1: [Construye una cadena de búsqueda simple y relevante con estas palabras clave y sus sinónimos para bases de datos científicas como Scopus]
            Cadena de búsqueda 2: [Otra cadena de búsqueda optimizada con palabras clave relevantes]
            Cadena de búsqueda 3: [Otra cadena de búsqueda similar]

        Nota:
        1. Asegúrate de que las palabras clave sean relevantes para el tema, compuestas por un máximo de dos palabras y priorizando las que sean de una sola palabra.
        2. Mantén los términos y cadenas en inglés para mayor alcance científico.
        3. Evita usar términos demasiado generales que puedan producir resultados irrelevantes.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en escribir articulos cientificos de mapeos sistematico.."},
                {"role": "user", "content": prompt}
            ]
        )
        return self.parse_response(response['choices'][0]['message']['content'])
    
    def parse_response(self, response_content):
        # Inicializa el diccionario para almacenar cada categoría
        categories = {
            "Poblacion": {},
            "Intervencion": {},
            "Resultado": {}
        }
        search_strings = {
            "Cadena_de_busqueda_1": "",
            "Cadena_de_busqueda_2": "",
            "Cadena_de_busqueda_3": ""
        }

        # Expresiones regulares para capturar las cadenas de búsqueda
        search_string_pattern = re.compile(r"Cadena de búsqueda (\d+):\s*(.+)")

        # Divide el contenido en líneas y utiliza un puntero para la categoría actual
        lines = response_content.splitlines()
        current_category = None
        term_index = 1

        # Recorre cada línea para clasificar los términos en las categorías correspondientes
        for line in lines:
            line = line.strip()
            
            # Detecta el inicio de cada categoría y resetea el índice de términos
            if line.startswith("Población:"):
                current_category = "Poblacion"
                term_index = 1
            elif line.startswith("Intervención:"):
                current_category = "Intervencion"
                term_index = 1
            elif line.startswith("Resultado:"):
                current_category = "Resultado"
                term_index = 1
            elif line.startswith("Cadenas de búsqueda:"):
                current_category = "Cadenas_de_busqueda"
                term_index = 1
            elif current_category == "Cadenas_de_busqueda" and search_string_pattern.match(line):
                # Extrae la cadena de búsqueda usando la expresión regular
                match = search_string_pattern.match(line)
                if match:
                    string_number = match.group(1).strip()
                    search_string = match.group(2).strip()
                    search_strings[f"Cadena_de_busqueda_{string_number}"] = search_string
            elif current_category and line and current_category != "Cadenas_de_busqueda":
                # Guarda cada sinónimo en la categoría actual
                categories[current_category][f"Sinonimo_{term_index}"] = line
                term_index += 1

        # Construimos el resultado final en el formato solicitado
        result = {
            "Intervencion": categories["Intervencion"],
            "Poblacion": categories["Poblacion"],
            "Resultado": categories["Resultado"],
            "Cadena_de_busqueda_1": search_strings["Cadena_de_busqueda_1"],
            "Cadena_de_busqueda_2": search_strings["Cadena_de_busqueda_2"],
            "Cadena_de_busqueda_3": search_strings["Cadena_de_busqueda_3"]
            
        }

        return result