import os
import requests
from flask import jsonify
from typing import Dict, Any, List, Optional
from urllib.parse import quote
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ScopusService:
    """
    Servicio para interactuar con la API de Scopus
    """
    
    def __init__(self):
        """
        Inicializa el servicio con las configuraciones necesarias
        """
        self.api_key = os.getenv('SCOPUS_API_KEY')
        self.endpoint = "https://api.elsevier.com/content/search/scopus"
        
        if not self.api_key:
            print("Advertencia: SCOPUS_API_KEY no está configurada")

    def test_scopus_connection(self) -> bool:
        """
        Prueba la conexión con Scopus usando una query simple
        """
        test_query = "computer science"
        headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }
        params = {
            "query": test_query,
            "count": "1"
        }
        
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            print(f"Test Connection Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return response.status_code == 200
        except Exception as e:
            print(f"Test Connection Error: {str(e)}")
            return False

    def generar_respuesta_fuentes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera respuesta con resultados de búsqueda de Scopus
        """
        try:
            # Extraer y validar datos
            query = data.get('query', '')
            if not query:
                return {"error": "Query no proporcionado"}

            anio_inicio = int(data.get('anio_inicio', 0))
            anio_fin = int(data.get('anio_fin', 0))
            
           
            resultados = self.buscar(query)
            
            return {
                "resultados": resultados,
                "query_utilizado": query,
                "total_encontrados": len(resultados) if isinstance(resultados, list) else 0,
                "estadisticas": self._generar_estadisticas(resultados) if isinstance(resultados, list) and resultados else {}
            }

        except Exception as e:
            print(f"Error en generar_respuesta_fuentes: {str(e)}")
            return {
                "error": str(e),
                "query_utilizado": query if 'query' in locals() else "No disponible",
                "resultados": []
            }

    def buscar(self, query: str, count: int = 10, start: int = 0) -> List[Dict[str, Any]]:
        """
        Realiza búsqueda en Scopus
        """
        try:
            query = str(query).strip()
            
            headers = {
                "X-ELS-APIKey": self.api_key,
                "Accept": "application/json"
            }
            
            params = {
                "query": query,
                "count": str(min(count, 25)),
                "start": str(start),
                "field": "dc:title,dc:creator,prism:publicationName,prism:coverDate,prism:doi,citedby-count,subtypeDescription,prism:url,author,authkeywords,dc:description",
                "sort": "-citedby-count"
            }

            print(f"Realizando búsqueda con parámetros:")
            print(f"Query: {query}")
            print(f"Params: {params}")

            response = requests.get(
                self.endpoint,
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_results(data)
            else:
                print(f"Error en la API: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return []

        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            return []

    def _parse_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Procesa resultados de la búsqueda
        """
        results = []
        try:
            entries = data.get("search-results", {}).get("entry", [])
            print(f"Procesando {len(entries)} resultados")
            
            for entry in entries:
                try:
                    # Procesar autores
                    authors = []
                    
                    # Intentar obtener autores del campo dc:creator
                    creator = entry.get("dc:creator")
                    if creator:
                        if isinstance(creator, str):
                            authors = [name.strip() for name in creator.split(',')]
                        elif isinstance(creator, list):
                            authors = creator

                    # Si no hay autores en dc:creator, intentar con el campo author
                    if not authors and "author" in entry:
                        author_data = entry["author"]
                        if isinstance(author_data, list):
                            for author in author_data:
                                if isinstance(author, dict):
                                    given_name = author.get("given-name", "")
                                    surname = author.get("surname", "")
                                    if given_name or surname:
                                        full_name = f"{given_name} {surname}".strip()
                                        authors.append(full_name)

                    # Procesar keywords
                    keywords = []
                    if "authkeywords" in entry:
                        kw = entry.get("authkeywords", "")
                        if isinstance(kw, str):
                            keywords = [k.strip() for k in kw.split(';') if k.strip()]
                        elif isinstance(kw, list):
                            keywords = kw

                    # Construir resultado
                    result = {
                        "title": str(entry.get("dc:title", "")).strip(),
                        "authors": authors if authors else ["Autor no disponible"],
                        "journal": str(entry.get("prism:publicationName", "No disponible")),
                        "year": str(entry.get("prism:coverDate", ""))[:4] if entry.get("prism:coverDate") else "Año no disponible",
                        "doi": str(entry.get("prism:doi", "DOI no disponible")),
                        "abstract": str(entry.get("dc:description", "No disponible")),
                        "keywords": keywords,
                        "cited_by_count": int(entry.get("citedby-count", 0)),
                        "document_type": str(entry.get("subtypeDescription", "No especificado")),
                        "url": str(entry.get("prism:url", "URL no disponible"))
                    }

                    # Limpiar valores vacíos
                    result = {k: v for k, v in result.items() if v is not None and v != "" and v != []}
                    results.append(result)

                except Exception as e:
                    print(f"Error procesando entrada individual: {str(e)}")
                    continue

            print(f"Total de resultados procesados: {len(results)}")
            return results

        except Exception as e:
            print(f"Error general procesando resultados: {str(e)}")
            return []

    def _generar_estadisticas(self, resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Genera estadísticas de los resultados
        """
        try:
            if not resultados:
                return {}

            # Inicializar contadores
            publicaciones_por_revista = {}
            publicaciones_por_anio = {}
            tipos_documento = {}
            total_citaciones = 0
            keywords_frecuencia = {}

            # Procesar cada resultado
            for resultado in resultados:
                # Estadísticas por revista
                revista = resultado.get('journal', 'No especificado')
                publicaciones_por_revista[revista] = publicaciones_por_revista.get(revista, 0) + 1
                
                # Estadísticas por año
                anio = resultado.get('year', 'No especificado')
                publicaciones_por_anio[anio] = publicaciones_por_anio.get(anio, 0) + 1
                
                # Estadísticas por tipo de documento
                tipo = resultado.get('document_type', 'No especificado')
                tipos_documento[tipo] = tipos_documento.get(tipo, 0) + 1
                
                # Conteo de citaciones
                total_citaciones += resultado.get('cited_by_count', 0)
                
                # Frecuencia de keywords
                for keyword in resultado.get('keywords', []):
                    keywords_frecuencia[keyword] = keywords_frecuencia.get(keyword, 0) + 1

            # Ordenar revistas por número de publicaciones
            revistas_principales = dict(
                sorted(
                    publicaciones_por_revista.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            )

            return {
                "total_publicaciones": len(resultados),
                "total_citaciones": total_citaciones,
                "promedio_citaciones": round(total_citaciones / len(resultados), 2) if resultados else 0,
                "revistas_principales": revistas_principales,
                "publicaciones_por_anio": dict(sorted(publicaciones_por_anio.items())),
                "tipos_documento": tipos_documento,
                "keywords_principales": dict(sorted(
                    keywords_frecuencia.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10])
            }

        except Exception as e:
            print(f"Error generando estadísticas: {str(e)}")
            return {
                "error": f"Error al generar estadísticas: {str(e)}"
            }