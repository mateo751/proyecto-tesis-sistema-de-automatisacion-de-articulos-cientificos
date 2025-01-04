import openai
import os
import re

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generar_metodo_pico_Form(self, tema, pregunta_investigacion, sub_pregunta_1, sub_pregunta_2, sub_pregunta_3):
        prompt = f"""
        Tengo el siguiente tema de investigación "{tema}" y la siguiente pregunta de investigación: "{pregunta_investigacion}".
        Y estas tres sub-preguntas relacionadas:
        1. {sub_pregunta_1}
        2. {sub_pregunta_2}
        3. {sub_pregunta_3}
        
        Usando la estructura PICO (Población, Intervención, Resultado), por favor genera una respuesta para cada uno de estos elementos con el siguiente formato exacto:
        - Población:
            [Una palabra clave] 
            [1 sinónimos],
            [2 sinónimos],
            [3 sinónimos]

        - Intervención:
            [Una palabra clave] 
            [1 sinónimos],
            [2 sinónimos],
            [3 sinónimos]

        - Resultado:
            [Una palabra clave] 
            [1 sinónimos],
            [2 sinónimos],
            [3 sinónimos]
        
        - Cadena de busqueda:
            Cadena de busqueda simple: [una cadena de busquedas simple con las palabras y sininmos encontrados para la base de datos de Scopus]
            
        Nota: Asegúrate de que los términos, sinónimos y términos relacionados estén en inglés.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en metodología de investigación."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Procesar el contenido de la respuesta en JSON
        content = response['choices'][0]['message']['content']
        pico_data = self.parse_response(content)
        
        return pico_data

    def parse_response(self, response_text):
        # Extraer y estructurar los datos de Población, Intervención, Resultado y Cadena de búsqueda
        pico_data = {}
        
        # Ejemplo simple de extracción usando regex
        pico_data['Poblacion'] = re.findall(r'- Población:\n\s*\[(.*?)\]', response_text)
        pico_data['Intervencion'] = re.findall(r'- Intervención:\n\s*\[(.*?)\]', response_text)
        pico_data['Resultado'] = re.findall(r'- Resultado:\n\s*\[(.*?)\]', response_text)
        pico_data['CadenasBusqueda'] = re.findall(r'Cadena de busqueda simple: \[(.*?)\]', response_text)
        
        return pico_data
