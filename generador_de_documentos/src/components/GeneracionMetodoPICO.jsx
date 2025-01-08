import { useState } from 'react';
import { crearMetodoPico } from '../service/metodoPicoService.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionMetodoPICO.css';

const GeneracionMetodoPICO = () => {
  const [tema, setTema] = useState('');
  const [preguntaInvestigacion, setPreguntaInvestigacion] = useState('');
  const [subPregunta1, setSubPregunta1] = useState('');
  const [subPregunta2, setSubPregunta2] = useState('');
  const [subPregunta3, setSubPregunta3] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [picoResponse, setPicoResponse] = useState(null); // Estado para almacenar el picoResponse

  const handleSubmit = async (e) => {
    e.preventDefault();  // Evita que la página se recargue al enviar el formulario

    const metodoPico = {
      tema,
      pregunta_investigacion: preguntaInvestigacion,
      sub_pregunta_1: subPregunta1,
      sub_pregunta_2: subPregunta2,
      sub_pregunta_3: subPregunta3
    };

    try {
      const response = await crearMetodoPico(metodoPico);
      setMensaje(response.mensaje);  // Mostramos el mensaje de éxito del backend
      setPicoResponse(response.pico_response);  // Guardamos el picoResponse en el estado
    } catch (error) {
      console.error('Error al enviar los datos', error);
      setMensaje('Error al enviar los datos');
    }
  };

  return (
    <div className="form-container">
      <div className="card-body">
        <h1 className="form-title">Datos informativos del artículo</h1>
        <p className="form-description">Buscar palabras clave sobre el trabajo de investigación</p>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Título</label>
            <input
              type="text"
              className="form-control"
              value={tema}
              onChange={(e) => setTema(e.target.value)}
              placeholder="Ingresa el Tema a Investigar"
              required
            />
          </div>
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
          <button type="submit" className="btn-submit">Generación de método PICO</button>
        </form>
        {mensaje && <p className="text-center mt-3">{mensaje}</p>}
        {picoResponse && (
          <div className="mt-4 text-center">
            <h3>Respuesta PICO Generada:</h3>
            {/* Si picoResponse es un array, mapea los elementos */}
            {Array.isArray(picoResponse) ? (
              <div className="row">
                {picoResponse.map((responseItem, index) => (
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
              <p className="card-text" >{picoResponse}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GeneracionMetodoPICO;
