from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import base64
from io import BytesIO
import logging

class GenerarMetodosMaterialesService:
    def __init__(self, mongo):
        self.mongo = mongo
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_mapping_document(self, investigation_id):
        """
        Genera el documento de mapeo sistemático para una investigación.
        """
        try:
            self.logger.info(f"Iniciando generación de documento para investigation_id: {investigation_id}")
            
            # Obtener los datos de la investigación
            investigation = self.mongo.db.InvestigacionForm.find_one({'id': investigation_id})
            
            if not investigation:
                self.logger.error(f"No se encontró la investigación con ID: {investigation_id}")
                return {
                    'success': False,
                    'error': 'Investigación no encontrada'
                }

            # Procesar datos
            self.logger.info("Procesando estadísticas y palabras clave")
            stats = self._process_stats(investigation)
            keywords = self._process_keywords(investigation)
            
            try:
                # Generar PDF
                self.logger.info("Generando PDF")
                pdf_buffer = self._generate_pdf(investigation, stats, keywords)
                pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode()

                # Actualizar en la base de datos
                self.logger.info("Actualizando documento en la base de datos")
                self.mongo.db.InvestigacionForm.update_one(
                    {'id': investigation_id},
                    {
                        '$set': {
                            'mapping_document': pdf_base64,
                            'generated_at': datetime.now()
                        }
                    }
                )

                return {
                    'success': True,
                    'document': pdf_base64,
                    'statistics': stats
                }

            except Exception as e:
                self.logger.error(f"Error al generar PDF: {str(e)}")
                raise

        except Exception as e:
            self.logger.error(f"Error en generate_mapping_document: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _process_keywords(self, investigation):
        """
        Procesa y extrae las palabras clave de la investigación.
        """
        try:
            keywords = []
            
            if 'pico_response' in investigation:
                pico = investigation['pico_response']
                
                # Procesar Intervencion
                if 'Intervencion' in pico and isinstance(pico['Intervencion'], dict):
                    for i in range(1, 4):
                        key = f'Sinonimo_{i}'
                        if key in pico['Intervencion']:
                            value = str(pico['Intervencion'][key]).strip()
                            if value.startswith('- '):
                                value = value[2:]
                            keywords.append(value.rstrip(','))
                            self.logger.info(f"Added keyword from Intervencion {key}: {value}")

                # Procesar Poblacion
                if 'Poblacion' in pico and isinstance(pico['Poblacion'], dict):
                    for i in range(1, 4):
                        key = f'Sinonimo_{i}'
                        if key in pico['Poblacion']:
                            value = str(pico['Poblacion'][key]).strip()
                            if value.startswith('- '):
                                value = value[2:]
                            if ',' in value:
                                sub_keywords = [k.strip() for k in value.split(',')]
                                keywords.extend(sub_keywords)
                            else:
                                keywords.append(value.rstrip(','))
                            self.logger.info(f"Added keyword from Poblacion {key}: {value}")

                # Procesar Resultado
                if 'Resultado' in pico and isinstance(pico['Resultado'], dict):
                    for i in range(1, 4):
                        key = f'Sinonimo_{i}'
                        if key in pico['Resultado']:
                            value = str(pico['Resultado'][key]).strip()
                            if value.startswith('- '):
                                value = value[2:]
                            keywords.append(value.rstrip(','))
                            self.logger.info(f"Added keyword from Resultado {key}: {value}")

            # Eliminar duplicados y valores vacíos
            keywords = list(dict.fromkeys(filter(None, keywords)))
            self.logger.info(f"Final keywords list: {keywords}")
            return keywords
            
        except Exception as e:
            self.logger.error(f"Error processing keywords: {str(e)}")
            return []

    def _process_stats(self, investigation):
        """
        Procesa las estadísticas de la investigación.
        """
        try:
            stats = {
                'total_scopus': 0,
                'total_wos': 0,
                'total_pubmed': 0,
                'total_publications': 0,
                'keywords_stats': {},
                'duplicates': 0,
                'filtered_out': 0,
                'final_selected': 0
            }

            fuentes_response = investigation.get('fuentes_response', {})
            
            if isinstance(fuentes_response, dict) and 'search-results' in fuentes_response:
                entries = fuentes_response['search-results'].get('entry', [])
                stats['total_scopus'] = len(entries)
                stats['total_publications'] = stats['total_scopus']
                
                # Procesar estadísticas por palabra clave
                keywords = self._process_keywords(investigation)
                for entry in entries:
                    if 'keyword' in entry:
                        for keyword in keywords:
                            if keyword.lower() in entry.get('keyword', '').lower():
                                stats['keywords_stats'][keyword] = stats['keywords_stats'].get(keyword, 0) + 1

            self.logger.info(f"Processed stats: {stats}")
            return stats
            
        except Exception as e:
            self.logger.error(f"Error processing stats: {str(e)}")
            raise

    def _generate_pdf(self, investigation, stats, keywords):
        """
        Genera el documento PDF con el contenido del mapeo sistemático.
        """
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Obtener estilos
            styles = getSampleStyleSheet()
            # Lista para el contenido
            story = []
            
            # Primero, vamos a formatear las palabras clave para el texto
            keyword_text = ""
            for i, keyword in enumerate(keywords[:5], 1):  # Tomamos hasta 5 palabras clave
                keyword_text += f"i) {keyword}"
                if i < len(keywords[:5]):
                    keyword_text += ", "
            
            # Obtener las cadenas de búsqueda del pico_response
            search_strings = []
            if 'pico_response' in investigation:
                for i in range(1, 4):
                    key = f'Cadena_de_busqueda_{i}'
                    if key in investigation['pico_response']:
                        search_strings.append(investigation['pico_response'][key])
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading1'],
                fontSize=14,
                alignment=TA_LEFT,
                spaceAfter=12
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            )
            
            

            story.append(Paragraph(f"{investigation['tema']:}: Un Estudio de Mapeo", title_style))
            story.append(Spacer(1, 20))

            # Contenido principal
            normal_style = styles['Normal']
            heading_style = styles['Heading1']

            # 1.Metodos y materiales
            story.append(Paragraph("1.MATERIALES Y MÉTODOS", heading_style))
            story.append(Paragraph(f"""
                                   Esta revisión sistemática (RS) se basa en las directrices propuestas en [Referencias], 
                                   el principal objetivo es la realización de un análisis del panorama actual de investigaciones 
                                   e intervenciones relacionadas a los enfoques sobre aplicaciones de software para el registro 
                                   y seguimiento de {investigation['tema']}. Esta revisión incluye las etapas de planificación y ejecución. 
                                   La primera aborda la definición de las preguntas de investigación que especifica la intervención de interés, 
                                   el proceso de búsqueda, y la definición de los criterios de selección de los artículos: 
                                   La segunda etapa implementa el proceso de selección de las investigaciones relevantes al objeto de estudio, 
                                   a través de la aplicación de los criterios de selección y la extracción de datos para obtener los resultados de esta revisión sistemática.
                                   """, normal_style))
            story.append(Spacer(1, 20))
            
            # Planificación
            story.append(Paragraph("A. Planificación", heading_style))
            story.append(Paragraph(f"""
                                La intención de esta investigación se regirá a la pregunta de investigación principal (PI):
                                {investigation['pregunta_investigacion']}
                                """, normal_style))
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"""
                                La PI busca localizar documentos relevantes sobre el tema propuesto; para lograr este objetivo, 
                                la PI se divide en tres sub- preguntas de investigación.
                                """, normal_style))
            
             


            # Sub-preguntas
            for i, key in enumerate(['sub_pregunta_1', 'sub_pregunta_2', 'sub_pregunta_3'], 1):
                story.append(Paragraph(f"PI{i}: {investigation[key]}", normal_style))
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"""
                                Para realizar el proceso de búsqueda de publicaciones científicas que contribuyan al análisis del objeto de estudio, 
                                se considera el uso de tres bases de datos indexadas: Scopus, Web of Science y IEEE. 
                                Las dos primeras son bases de datos bibliográficas de resúmenes y citas de artículos de revistas científicas y 
                                la tercera es un motor de búsqueda de referencias bibliográficas que permite consultar los contenidos de las bases de datos SCIENCEDIRECT. 
                                Estas bases se complementan debido a que incluyen artículos parciales de conferencias que son relevantes para nuestro estudio. 
                                El proceso de búsqueda consiste en la selección de palabras claves, que se extraen de la pregunta de investigación: 
                                {keyword_text}. 
                                Palabras que permiten identificar sinónimos y términos relacionados al objeto de estudio, 
                                que al combinarse forman la cadena de búsqueda, cuyo fin es identificar artículos relevantes a la investigación. 
                                El periodo de búsqueda de las publicaciones relevantes se realizó entre los años [rango de las publicación inicial - [rango de las publicación final], 
                                debido a la rapidez en la que actualmente se producen los cambios tecnológicos.
                                """, normal_style))
            story.append(Paragraph(f"""
                                Una vez encontrados los artículos, se utilizan criterios de inclusión y exclusión para avanzar con el proceso de preselección y selección de artículos relevantes. 
                                Los criterios utilizados en esta revisión sistemática son:
                                """, normal_style))
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"""
                                Criterios de inclusión
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios en idioma inglés.
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios relacionados con el objeto de investigación.
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios de texto completo.
                                """, normal_style))
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"""
                                Criterios de exclusión
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios duplicados.
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios en donde no se desarrolla ningún aplicativo.
                                """, normal_style))
            story.append(Paragraph(f"""
                                * Estudios de revisión, libros o capítulos de libros.
                                """, normal_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph("B. Ejecución", heading_style))
            story.append(Paragraph(f"""
                                El proceso de ejecución empieza con la aplicación de la cadena de búsqueda inicial en las distintas bases de datos indexadas con el fin de ir refinado la cadena 
                                y encontrar los artículos relevantes al objeto de estudio.
                                """, normal_style))
            

           
            # Crear el párrafo con los datos dinámicos
            story.append(Paragraph(f"""
                En la primera iteración de búsqueda en las bases de datos bibliográficas se obtuvieron los siguientes 
                números de publicaciones en Scopus {stats['total_scopus']}, en Web of Science se encontraron 
                {stats['total_wos']} y en IEEE {stats['total_pubmed']}, aplicadas a los años {investigation.get('rango_inicial', '[No especificado]')} 
                hasta {investigation.get('rango_final', '[No especificado]')}. Después de una serie de iteraciones de 
                prueba y revisiones se identificaron los términos y sinónimos relacionados: {keyword_text}. 
                El modelo estándar de la cadena de búsqueda se expresa de la siguiente manera:
                {search_strings[0] if search_strings else '[Cadena de búsqueda no especificada]'}
                Una vez aplicada la cadena de búsqueda refinada se encontraron estudios primarios a la investigación y, 
                a fin de maximizar la exhaustividad de la búsqueda, se revisaron las referencias de estos estudios con el objetivo de identificar otros 
                estudios relevantes (técnica de búsqueda conocida como "bola de nieve" [Referencias][Referencias]). De acuerdo, con la Fig. 1 que muestra 
                el detalle del proceso de preselección y selección de artículos relevantes, en primer lugar, se identificaron en Scopus {stats['total_scopus']}, en 
                WOS {stats['total_wos']} y en IEEE {stats['total_pubmed']} publicaciones, dando un total de [total de las publicaciones] publicaciones. 
                Luego se procedió a eliminar los artículos duplicados, se obtuvieron [total de las publicaciones documentos duplicados] estudios repetidos en las distintas bases de datos, 
                que al consolidarse resultaron en {investigation['tema']} estudios por analizar. Una primera aproximación de estudios relevantes es su preselección. En primer lugar, 
                se descartaron artículos cuyo idioma era diferente al inglés, para luego analizar el título, el resumen y las palabras claves de cada artículo con el fin de verificar 
                si están relacionados con el objeto de estudio. Se eliminaron [artículos eliminados] artículos después de esta evaluación y se obtuvieron [revisión completa] artículos 
                para su revisión completa. Para la selección de artículos se analizó minuciosamente el texto completo, a fin de conocer si el artículo estaba estrechamente relacionado 
                al objeto de estudio, o si se desarrolló algún aplicativo que pueda verificar la construcción de una herramienta como un requisito mínimo para ser seleccionado. 
                En este proceso se aplicaron los criterios de inclusión y exclusión de estudios. Para evitar la subjetividad, las actividades de revisión de artículos y de extracción 
                de datos fueron realizadas por dos revisores, de forma independiente. Si un artículo no se incluía, se mencionaba la razón de su exclusión, con este análisis 
                se eliminaron [artículos eliminados] artículos, obteniendo [artículos utilizados] estudios usados para la extracción de datos.
            """, normal_style))

            # Palabras clave
            story.append(Spacer(1, 20))
            story.append(Paragraph("B. Palabras Clave", heading_style))
            
            if keywords and len(keywords) > 0:
                keywords_data = [['Categoría', 'Término']]
                for i, keyword in enumerate(keywords, 1):
                    keywords_data.append([f'Palabra clave {i}', keyword])

                keywords_table = Table(keywords_data, colWidths=[doc.width*0.3, doc.width*0.7])
                keywords_table.setStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                ])
                story.append(keywords_table)
            else:
                story.append(Paragraph("No se encontraron palabras clave.", normal_style))

            # Estadísticas
            story.append(Spacer(1, 20))
            story.append(Paragraph("C. Resultados de la Búsqueda", heading_style))
            
            stats_data = [
                ['Base de datos', 'Total de documentos'],
                ['Scopus', str(stats['total_scopus'])],
                ['Web of Science', str(stats['total_wos'])],
                ['PubMed', str(stats['total_pubmed'])],
                ['Total', str(stats['total_publications'])]
            ]

            stats_table = Table(stats_data, colWidths=[doc.width*0.5, doc.width*0.5])
            stats_table.setStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ])
            story.append(stats_table)

            # Estadísticas por palabra clave
            if stats['keywords_stats']:
                story.append(Spacer(1, 20))
                story.append(Paragraph("D. Frecuencia de Palabras Clave", heading_style))
                
                keyword_stats_data = [['Palabra Clave', 'Frecuencia']]
                for keyword, count in stats['keywords_stats'].items():
                    keyword_stats_data.append([keyword, str(count)])

                keyword_stats_table = Table(keyword_stats_data, colWidths=[doc.width*0.7, doc.width*0.3])
                keyword_stats_table.setStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                ])
                story.append(keyword_stats_table)

            # Generar PDF
            doc.build(story)
            buffer.seek(0)
            return buffer

        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}")
            raise

    def get_document(self, investigation_id):
        """
        Recupera un documento existente de la base de datos.
        """
        try:
            investigation = self.mongo.db.InvestigacionForm.find_one(
                {'id': investigation_id},
                {
                    'mapping_document': 1,
                    'tema': 1
                }
            )
            
            if not investigation or 'mapping_document' not in investigation:
                self.logger.error(f"Documento no encontrado para investigation_id: {investigation_id}")
                return {
                    'success': False,
                    'error': 'Documento no encontrado'
                }
                
            filename = f"mapeo_sistematico_{str(investigation_id)}.pdf"
            
            return {
                'success': True,
                'document': investigation['mapping_document'],
                'filename': filename,
                'content_type': 'application/pdf'
            }
        except Exception as e:
            self.logger.error(f"Error en get_document: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }