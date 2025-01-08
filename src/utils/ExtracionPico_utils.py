import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def extraer_terminos_pico(tema):
    # Tokenización 
    tokens = word_tokenize(tema)
    
    # Lematización
    lematizador = WordNetLemmatizer()
    lemas = [lematizador.lemmatize(token) for token in tokens]
    # Lematización
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Filtrar palabras comunes
    stop_words = ["de", "el", "están", "para", "que", "se", "un", "una", 
                  "y", "en", "los", "las", "del", "por", "al", "con", 
                  "como", "lo", "la", "a", "su", "sus", "más", "pero", 
                  "o", "si", "sí", "no", "porque", "sobre", "entre", 
                  "hasta", "desde", "durante", "ante", "tras", "mediante",
                  "bajo", "encima", "contra", "hacia", "dentro", "fuera",
                  "excepto", "según", "aunque", "siempre", "nunca",
                  "jamás", "también", "además", "así", "asimismo",
                  "mientras", "cuando", "donde", "quien", "cual",
                  "cómo", "cuánto", "cuándo", "cuál", "cuáles",
                  "qué", "porqué", "para", "para que", "porque",
                  "por qué", "a pesar de", "a causa de", "a fin de",
                  "a fin de que", "a menos que", "a no ser que", "aunque",
                  "como si", "con tal de que", "con tal que", "cuando",
                  "de manera que", "de modo que", "después de que",
                  "en caso de que", "en cuanto", "en el caso de que",
                  "en el momento en que", "en cuanto", "en cuanto a que",
                  "en tanto que", "hasta que", "luego de que",
                  "mientras que", "para que", "puesto que", "siempre que",
                  "sin que", "tan pronto como", "tanto que", "a pesar de que",
                  "aunque", "como si", "con tal de que", "con tal que", "cuando",
                  "de manera que", "de modo que", "después de que", "en caso de que",
                  "en cuanto", "en el caso de que", "en el momento en que", "en cuanto",
                  "en cuanto a que", "en tanto que", "hasta que", "luego de que", "mientras que",
                  "para que", "puesto que", "siempre que", "sin que"]
    lemmas = [lemma for lemma in lemmas if lemma not in stop_words]
    
    # Eliminar palabras repetidas
    lemmas = list(set(lemmas))
    
    # Unir los lemas en un solo texto
    texto_lematizado = ' '.join(lemmas)
    
    # Extracción de términos clave basada en TF-IDF
    vectorizer = TfidfVectorizer()
    matriz_tfidf = vectorizer.fit_transform([texto_lematizado])
    nombres_caracteristicas = vectorizer.get_feature_names_out()
    
    # Obtener los pesos TF-IDF de cada término
    pesos_tfidf = matriz_tfidf.toarray()[0]
    
    # Crear un diccionario de términos y sus pesos TF-IDF
    pesos_terminos = dict(zip(nombres_caracteristicas, pesos_tfidf))
    
    # Ordenar los términos por su peso TF-IDF en orden descendente
    terminos_ordenados = sorted(pesos_terminos.items(), key=lambda x: x[1], reverse=True)
    
    # Obtener los términos clave principales
    terminos_principales = [(termino, peso) for termino, peso in terminos_ordenados[:5]]
   
    return terminos_principales

