import { useState } from 'react';
import { crearPregunta } from '../service/preguntaService';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionPreguntas.css';

const GeneracionPregunta = () => {
  const [programaEstudio, setProgramaEstudio] = useState('');
  const [enfoqueGeneral, setEnfoqueGeneral] = useState('');
  const [identificarProblema, setIdentificarProblema] = useState('');
  const [idioma, setIdioma] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [preguntaResponse, setPreguntaResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();  // Evita que la página se recargue al enviar el formulario

    const pregunta = {
      programa_de_estudio: programaEstudio,
      enfoque_general:enfoqueGeneral,
      identificar_problema:identificarProblema,
      idioma
    };

    try {
      const response = await crearPregunta(pregunta);
      setMensaje(response.mensaje);  // Mostramos el mensaje de éxito del backend
      setPreguntaResponse(response.pregunta_response);  // Guardamos el picoResponse en el estado
    } catch (error) {
      console.error('Error al enviar los datos', error);
      setMensaje('Error al enviar los datos');
    }
  };
  return (
    <div className="form-container">
       <div className="card-body">
      <h1 className="form-title">Generar preguntas de investigacion</h1>
      <p className="form-description">Generar ideas adicionales sobre preguntas que puedes inclir en un trabajo de investigación</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="studyProgram" className="form-label">Tema de Estudio</label>
          <input type="text"className="form-control" value={programaEstudio} onChange={(e) => setProgramaEstudio(e.target.value)} placeholder="Ciencias Computación" required />
        </div>

        <div className="form-group">
          <label htmlFor="subject" className="form-label">Enfoque General <span className="optional">(Opcional)</span></label>
          <textarea
                className="form-control"
                value={enfoqueGeneral}
                onChange={(e) => setEnfoqueGeneral(e.target.value)}
                placeholder="Considera los principales componentes del tema que podrían ser de interés para explorar más a fondo"
                required
              />
        </div>

        <div className="form-group">
          <label htmlFor="interests" className="form-label">Identificar Problemas a Resolver <span className="optional">(Opcional)</span></label>
          <textarea
                className="form-control"
                value={identificarProblema}
                onChange={(e) => setIdentificarProblema(e.target.value)}
                placeholder="Considera los principales componentes del tema que podrían ser de interés para explorar más a fondo"
                required
              />
        
        </div>

        <div className="form-group">
          <label htmlFor="language" className="form-label">Idioma <span className="optional">(Opcional)</span></label>
          <select className="form-control custom-select" id="language">
            <option value={idioma} onChange={(e) => setIdioma(e.target.value)}>ES-es</option>
            <option value={idioma} onChange={(e) => setIdioma(e.target.value)}>US-en</option>
          </select>
        </div>
        <button type="submit" className="btn-submit">generar</button>
      </form>
      {mensaje && <p className="text-center mt-3">{mensaje}</p>}
        {preguntaResponse && (
          <div className="mt-4 text-center">
            <h3>Respuesta preguntas Generada:</h3>
            {/* Si picoResponse es un array, mapea los elementos */}
            {Array.isArray(preguntaResponse) ? (
              <div className="row">
                {preguntaResponse.map((responseItem, index) => (
                  <div className="col-md-6" key={index}>
                    <div className="card">
                      <div className="card-body">
                        <h5 className="card-title">{responseItem.titulo}</h5>
                        <p className="card-text">{responseItem.descripcion}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              /* Si no es un array, simplemente lo muestra como texto */
              <p className="card-text" >{preguntaResponse}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GeneracionPregunta;
