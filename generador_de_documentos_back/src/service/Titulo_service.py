import openai
import os

class OpenAIService:
    def __init__(self):
        # Asegúrate de que la clave API esté en una variable de entorno
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generar_titulo(self, programa_de_estudio, asignatura, intereses, idioma):
        prompt = f"""
        Basándome en el programa de estudio '{programa_de_estudio}' aplicado a la asignatura '{asignatura}', y considerando el enfoque de interés '{intereses}', 
        genera 5 títulos de investigación científica para un estudio de mapeo sistemático.
        Utiliza la técnica de Revisión de literatura y considera las últimas tendencias y brechas de investigación en el campo. Para cada título aplica los siguentes requisitos, 
        
        Requisitos:

        Todos los títulos y análisis deben estar en '{idioma}'.
        Los títulos deben ser concisos pero informativos, idealmente entre 10 y 15 palabras.
        Incorpora términos clave relevantes al campo de estudio en los títulos.
        Evita repeticiones entre los títulos propuestos.
        Considera la factibilidad de la investigación al proponer los títulos.
        proporciona una respuesta con el siguiente formato exacto:

        Título de investigación:
        [Título propuesto]
        [Análisis (máximo 3 líneas):

        Relevancia y originalidad del título
        Alineación con el programa de estudio, asignatura e intereses
        Potencial impacto en el campo de estudio]



        
        NOTA: No incluyas ninguna introducción, conclusión o comentarios adicionales fuera del formato especificado.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en metodología de investigación."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']