import openai
import os

class OpenAIService:
    def __init__(self):
        # Asegúrate de que la clave API esté en una variable de entorno
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generar_metodo_pico(self, tema, pregunta_investigacion, sub_pregunta_1, sub_pregunta_2, sub_pregunta_3):
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
            Cadena de busqueda sinmple: [una cadena de busquedas simple con las palabras y sininmos encontrados para la base de datos de Scopus]
            
        Nota: Asegúrate de que los términos, sinónimos y términos relacionados estén en inglés.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en metodología de investigación."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']