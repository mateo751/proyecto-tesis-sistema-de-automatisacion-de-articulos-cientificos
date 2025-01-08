// src/components/FormularioCompleto.jsx
import { useState } from "react";
import { 
  crearInvestigacionForm, 
  generarDocumentoMapeo, 
} from '../service/investigacionesFormService';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionMetodoPICO.css';
import './css/TituloFormulario.css';

const FormularioCompleto = () => {
  // Estados para el formulario
  const [step, setStep] = useState(1);
  const [tema, setTema] = useState('');
  const [preguntaInvestigacion, setPreguntaInvestigacion] = useState('');
  const [subPregunta1, setSubPregunta1] = useState('');
  const [subPregunta2, setSubPregunta2] = useState('');
  const [subPregunta3, setSubPregunta3] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [cadenaBusqueda, setCadenaBusqueda] = useState('');
  const [queryModified, setQueryModified] = useState(false);
  const [accesoAbierto, setAccesoAbierto] = useState(false);
  const [anioInicio, setAnioInicio] = useState(2000);
  const [anioFin, setAnioFin] = useState(new Date().getFullYear());
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [picoResponse, setPicoResponse] = useState(null);
  const [mappingDocument, setMappingDocument] = useState(null);

  // Función para validar el formulario
  const validateForm = () => {
    if (!tema || !preguntaInvestigacion) {
      setError('Por favor complete los campos obligatorios');
      return false;
    }
    const finalQuery = selectedOption || cadenaBusqueda;
    if (!finalQuery || !queryModified) {
      setError('Por favor seleccione o modifique la cadena de búsqueda');
      return false;
    }
    if (anioInicio > anioFin) {
      setError('El año de inicio no puede ser mayor que el año final');
      return false;
    }
    return true;
  };

  // Manejador para avanzar al siguiente paso
  const handleNext = async () => {
    if (step === 2) {
      try {
        setLoading(true);
        setError(null);
        
        // En el paso 2, enviamos los datos básicos sin query
        const formData = {
          tema,
          pregunta_investigacion: preguntaInvestigacion,
          sub_pregunta_1: subPregunta1,
          sub_pregunta_2: subPregunta2,
          sub_pregunta_3: subPregunta3,
          anio_inicio: anioInicio,
          anio_fin: anioFin
        };
  
        console.log('Enviando datos iniciales:', formData);
        
        const response = await crearInvestigacionForm(formData);
        if (response.pico_response) {
          setPicoResponse(response.pico_response);
          setStep(3);
        } else {
          throw new Error('No se recibió respuesta PICO del servidor');
        }
      } catch (error) {
        console.error('Error:', error);
        setError(error.message || 'Error al procesar los datos');
      } finally {
        setLoading(false);
      }
    } else if (step === 3) {
      if (!selectedOption && !cadenaBusqueda) {
        setError('Por favor selecciona o ingresa una cadena de búsqueda');
        return;
      }
      setStep(4);
    } else {
      setStep(prev => prev + 1);
    }
  };

  // Manejador para retroceder al paso anterior
  const handlePrevious = () => {
    setStep(prev => prev - 1);
  };

  // Manejador para seleccionar una opción de búsqueda
  const handleOptionSelect = (e) => {
    const value = e.target.value;
    setSelectedOption(value);
    setCadenaBusqueda(value);
    setQueryModified(true);
    if (error) setError(null);
  };

  const handleFinalSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
  
    setLoading(true);
    setError(null);
  
    try {
      const finalQuery = selectedOption || cadenaBusqueda;
      const formData = {
        tema,
        pregunta_investigacion: preguntaInvestigacion,
        sub_pregunta_1: subPregunta1,
        sub_pregunta_2: subPregunta2,
        sub_pregunta_3: subPregunta3,
        anio_inicio: anioInicio,
        anio_fin: anioFin,
        query: finalQuery
      };
  
      const response = await crearInvestigacionForm(formData);
      
      // Verifica la estructura correcta de la respuesta
      if (response?.fuentes_response?.resultados) {
        setResultados(response.fuentes_response.resultados);
        setStep(5);
      } else {
        throw new Error('No se encontraron resultados');
      }
    } catch (error) {
      console.error('Error en submit:', error);
      setError(error.message || 'Error al guardar la investigación');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateDocument = async () => {
    try {
      setLoading(true);
      setError(null);
  
      // Primero crear/actualizar la investigación
      const investigacionResponse = await crearInvestigacionForm({
        tema,
        pregunta_investigacion: preguntaInvestigacion,
        sub_pregunta_1: subPregunta1,
        sub_pregunta_2: subPregunta2,
        sub_pregunta_3: subPregunta3,
        anio_inicio: anioInicio,
        anio_fin: anioFin,
        query: selectedOption || cadenaBusqueda
      });
  
      if (!investigacionResponse.id) {
        throw new Error('No se recibió el ID de la investigación');
      }
  
      // Luego generar el documento
      const documentResponse = await generarDocumentoMapeo(investigacionResponse.id);
  
      if (documentResponse.document) {
        setMappingDocument(documentResponse.document);
        setStep(6);
      } else if (documentResponse.error) {
        throw new Error(documentResponse.error);
      } else {
        throw new Error('No se pudo generar el documento');
      }
  
    } catch (err) {
      console.error('Error en la generación:', err);
      setError(err.message || 'Error al generar el documento');
    } finally {
      setLoading(false);
    }
  };
  // Manejador para descargar el documento
  const handleDownloadDocument = () => {
    try {
      if (!mappingDocument) {
        throw new Error('No hay documento para descargar');
      }
  
      // Crear Blob desde base64
      const binaryString = window.atob(mappingDocument);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const blob = new Blob([bytes], { type: 'application/pdf' });
      
      // Crear URL y enlace de descarga
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `mapeo_sistematico_${new Date().getTime()}.pdf`;
      
      // Simular clic y limpiar
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error al descargar:', error);
      setError('Error al descargar el documento: ' + error.message);
    }
  };
  
  const handleCopyToClipboard = async () => {
    try {
      if (!mappingDocument) {
        throw new Error('No hay documento para copiar');
      }
      
      await navigator.clipboard.writeText(mappingDocument);
      // Opcional: Mostrar mensaje de éxito
      alert('Documento copiado al portapapeles');
    } catch (error) {
      console.error('Error al copiar:', error);
      setError('Error al copiar al portapapeles: ' + error.message);
    }
  };


  return (
    <div className="formulario-completo">
      {/* Paso 1: Tema */}
      {step === 1 && (
        <div className="form-container">
          <h2>Su tema</h2>
          <p>Escriba su tema o idea...</p>
          <textarea
            value={tema}
            onChange={(e) => setTema(e.target.value)}
            placeholder="Ingresa tu tema aquí"
            className="tema-textarea"
          />
          <button 
            onClick={handleNext} 
            disabled={!tema} 
            className={`submit-button ${!tema ? 'disabled' : ''}`}
          >
            Próximo
          </button>
        </div>
      )}

      {/* Paso 2: Preguntas de Investigación */}
      {step === 2 && (
        <div className="form-container">
          <div className="card-body">
            <h1 className="form-title">Datos informativos del artículo</h1>
            <p className="form-description">Buscar palabras clave sobre el trabajo de investigación</p>
            
            <div className="mb-3">
              <label className="form-label">Pregunta de Investigación (PI)</label>
              <textarea
                className="form-control"
                value={preguntaInvestigacion}
                onChange={(e) => setPreguntaInvestigacion(e.target.value)}
                placeholder="Ingresa la Pregunta de Investigación"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Sub-Pregunta de Investigación (PI1)</label>
              <textarea
                className="form-control"
                value={subPregunta1}
                onChange={(e) => setSubPregunta1(e.target.value)}
                placeholder="Ingresa la Sub-Pregunta 1 de Investigación"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Sub-Pregunta de Investigación (PI2)</label>
              <textarea
                className="form-control"
                value={subPregunta2}
                onChange={(e) => setSubPregunta2(e.target.value)}
                placeholder="Ingresa la Sub-Pregunta 2 de Investigación"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Sub-Pregunta de Investigación (PI3)</label>
              <textarea
                className="form-control"
                value={subPregunta3}
                onChange={(e) => setSubPregunta3(e.target.value)}
                placeholder="Ingresa la Sub-Pregunta 3 de Investigación"
                required
              />
            </div>

            <div className="button-container">
              <button className="btn-submit" onClick={handlePrevious}>Anterior</button>
              <button 
                className="btn-submit" 
                onClick={handleNext}
                disabled={!preguntaInvestigacion || !subPregunta1 || !subPregunta2 || !subPregunta3}
              >
                {loading ? 'Procesando...' : 'Próximo'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Paso 3: Método PICO */}
      {step === 3 && (
        <div className="form-container">
          <h1>Matriz de la metodología PICO</h1>
          <p>Evalúa las palabras clave que puedan tener mejor impacto en la investigación</p>
          
          {picoResponse ? (
            <>
              <table className="table">
                <thead>
                  <tr>
                    <th></th>
                    <th>Términos principales</th>
                    <th>Sinónimos</th>
                    <th>Términos relacionados</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Intervención</td>
                    <td>{picoResponse?.Intervencion?.Sinonimo_1}</td>
                    <td>{picoResponse?.Intervencion?.Sinonimo_2}</td>
                    <td>{picoResponse?.Intervencion?.Sinonimo_3}</td>
                  </tr>
                  <tr>
                    <td>Población</td>
                    <td>{picoResponse?.Poblacion?.Sinonimo_1}</td>
                    <td>{picoResponse?.Poblacion?.Sinonimo_2}</td>
                    <td>{picoResponse?.Poblacion?.Sinonimo_3}</td>
                  </tr>
                  <tr>
                    <td>Resultado</td>
                    <td>{picoResponse?.Resultado?.Sinonimo_1}</td>
                    <td>{picoResponse?.Resultado?.Sinonimo_2}</td>
                    <td>{picoResponse?.Resultado?.Sinonimo_3}</td>
                  </tr>
                </tbody>
              </table>

              <h3>Su cadena de búsqueda</h3>
              <input
                type="text"
                placeholder="Escribe tu cadena aquí"
                value={selectedOption}
                className="tema-textarea"
                onChange={(e) => setSelectedOption(e.target.value)}
              />

              <div className="radio-options">
                {[1, 2, 3].map((num) => (
                  <label key={num} className="radio-label">
                    <input
                      type="radio"
                      value={picoResponse?.[`Cadena_de_busqueda_${num}`] || ''}
                      checked={selectedOption === picoResponse?.[`Cadena_de_busqueda_${num}`]}
                      onChange={handleOptionSelect}
                    />
                    <span>{picoResponse?.[`Cadena_de_busqueda_${num}`] || ''}</span>
                  </label>
                ))}
              </div>
            </>
          ) : (
            <p>Cargando datos de PICO...</p>
          )}

          <div className="button-container">
            <button onClick={handlePrevious}>Anterior</button>
            <button 
              onClick={handleNext}
              disabled={!selectedOption}
            >
              Próximo
            </button>
          </div>
        </div>
      )}

      {/* Paso 4: Búsqueda de fuentes */}
      {step === 4 && (
        <div className="form-container">
          <div className="card-body">
            <h1 className="form-title">Buscar fuentes</h1>
            <p className="form-description">
              Búsqueda de fuentes académicas relevantes para el tema.
            </p>

            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}

            <form onSubmit={handleFinalSubmit}>
              <div className="mb-3">
                <label className="form-label">Cadena de búsqueda</label>
                <select
                  className="form-control"
                  value={cadenaBusqueda}
                  onChange={(e) => {
                    setCadenaBusqueda(e.target.value);
                    setQueryModified(true);
                }}>
                  <option value="">{selectedOption}</option>
                </select>
                {!queryModified && (
                    <small className="text-warning">
                        * Por favor, revise y confirme la cadena de búsqueda
                    </small>
                )}
              </div>

              <div className="mb-3">
                <label className="form-label">
                  <input
                    type="checkbox"
                    checked={accesoAbierto}
                    onChange={() => setAccesoAbierto(!accesoAbierto)}
                  />
                  {' '}Mostrar solo fuentes de acceso abierto
                </label>
              </div>

              <div className="mb-3">
                <label className="form-label">Año de publicación</label>
                <div className="range-container">
                  <input
                    type="range"
                    min="2000"
                    max="2024"
                    value={anioInicio}
                    onChange={(e) => setAnioInicio(parseInt(e.target.value))}
                  />
                  <input
                    type="range"
                    min="2000"
                    max="2024"
                    value={anioFin}
                    onChange={(e) => setAnioFin(parseInt(e.target.value))}
                  />
                  <div className="range-values">
                    <span>{anioInicio}</span>
                    <span>{anioFin}</span>
                  </div>
                </div>
              </div>

              <div className="button-container">
                <button type="button" onClick={handlePrevious}>
                  Anterior
                </button>
                {/* En el paso 4, cambia el botón */}
                <button 
                    type="button"  // Cambiado a type="button"
                    onClick={handleFinalSubmit}
                    className="btn-submit"
                    disabled={loading || !cadenaBusqueda}
                >
                    {loading ? 'Buscando...' : 'Buscar fuentes'}
                </button>
              </div>
            </form>

           
          </div>
        </div>
      )}
      {step === 5 && (
        <div className="form-container">
          <div className="card-body">
            <h1 className="form-title">Resultados de la búsqueda</h1>
            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}

            <div className="results-header mb-4">
              <div className="search-stats">
                <p><strong>Total de publicaciones encontradas:</strong> {resultados.length}</p>
                <p><strong>Cadena de búsqueda utilizada:</strong> {selectedOption}</p>
                <p><strong>Rango de años:</strong> {anioInicio} - {anioFin}</p>
              </div>
            </div>

            {resultados && resultados.length > 0 ? (
              <div className="resultados-lista">
                {resultados.map((resultado, index) => (
                  <div key={index} className="card mb-3">
                    <div className="card-body">
                      <h3 className="card-title h5">{resultado.title}</h3>
                      <div className="article-details">
                        <p className="mb-2">
                          <strong>Autores:</strong> {
                            Array.isArray(resultado.authors) 
                              ? resultado.authors.join(', ') 
                              : 'No especificado'
                          }
                        </p>
                        <p className="mb-2">
                          <strong>Revista:</strong> {resultado.journal || 'No especificado'}
                        </p>
                        <p className="mb-2">
                          <strong>Año:</strong> {resultado.year || 'No especificado'}
                        </p>
                        <p className="mb-2">
                          <strong>Tipo de documento:</strong> {resultado.document_type || 'No especificado'}
                        </p>
                        <p className="mb-2">
                          <strong>Citaciones:</strong> {resultado.cited_by_count || 0}
                        </p>
                        {resultado.doi && (
                          <p className="mb-2">
                            <strong>DOI:</strong>{' '}
                            <a 
                              href={`https://doi.org/${resultado.doi}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary"
                            >
                              {resultado.doi}
                            </a>
                          </p>
                        )}
                        {resultado.abstract && resultado.abstract !== 'No disponible' && (
                          <p className="mb-2">
                            <strong>Resumen:</strong> {resultado.abstract}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-5">
                <p className="text-muted">
                  {loading ? 'Buscando resultados...' : 'No se encontraron resultados'}
                </p>
              </div>
            )}

            <div className="button-container mt-4">
              <button 
                className="btn btn-secondary me-2"
                onClick={handlePrevious}
              >
                Volver a la búsqueda
              </button>
              <button 
                className="btn btn-primary"
                onClick={handleGenerateDocument}
                disabled={loading || !resultados?.length}
              >
                {loading ? 'Generando...' : 'Generar Documento'}
              </button>
            </div>
          </div>
        </div>
      )}
        {step === 6 && (
        <div className="form-container">
          <div className="card-body">
            <h1 className="form-title">Documento de Mapeo Sistemático</h1>
            
            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}

            {loading ? (
              <div className="text-center py-5">
                <div className="spinner-border" role="status">
                  <span className="visually-hidden">Cargando...</span>
                </div>
                <p className="mt-2">Generando documento...</p>
              </div>
            ) : mappingDocument ? (
              <div className="documento-container">
                <div className="documento-controles mb-3">
                  <button 
                    className="btn btn-primary me-2"
                    onClick={handleDownloadDocument}
                  >
                    Descargar PDF
                  </button>
                  <button 
                    className="btn btn-secondary"
                    onClick={handleCopyToClipboard}
                  >
                    Copiar al Portapapeles
                  </button>
                </div>
                
                <div className="documento-preview border p-3">
                  {/* Visor de PDF */}
                  <iframe
                    src={`data:application/pdf;base64,${mappingDocument}`}
                    width="100%"
                    height="600px"
                    style={{ border: 'none' }}
                  />
                </div>
              </div>
            ) : (
              <div className="text-center py-5">
                <p className="text-muted">No se ha generado ningún documento aún</p>
              </div>
            )}

            <div className="button-container mt-4">
              <button 
                className="btn btn-secondary me-2"
                onClick={() => setStep(5)}
                disabled={loading}
              >
                Volver a Resultados
              </button>
              <button 
                className="btn btn-primary"
                onClick={() => setStep(1)}
                disabled={loading}
              >
                Nueva investigación
              </button>
            </div>
          </div>
        </div>
      )}
    </div>  
  );
};

export default FormularioCompleto;