import { useState } from 'react';
import { crearPregunta } from '../service/preguntaService';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionPreguntas.css';

const PreguntaFormulario = () => {
  
  const [enfoqueGeneral, setEnfoqueGeneral] = useState('');
  const [identificarProblema, setIdentificarProblema] = useState('');

  const [mensaje, setMensaje] = useState('');
  const [preguntaResponse, setPreguntaResponse] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();  // Evita que la página se recargue al enviar el formulario

    const pregunta = {
      
      enfoque_general:enfoqueGeneral,
      identificar_problema:identificarProblema,

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
  const handleProximoClick = () => {
    navigate('/preguntas/formulario'); // Redirige a la vista TemaEvaluacion
  };
  return (
    <div className="form-container">
       <div className="card-body">
      <h1 className="form-title">Sus preguntas de investigacion</h1>
      <p className="form-description">Por favor, escriba sus preguntas de investigacion. Puede ser con pocas palabras o
        preguntas corta que capture la esencia de lo que quieres escribir.</p>
        
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
      <form onSubmit={handleSubmit}>
        

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

        <button type="submit" disabled={[!enfoqueGeneral, !identificarProblema]}  className={`submit-button ${!enfoqueGeneral ? 'disabled' : ''}`}
        onClick={handleProximoClick}
        >
        generar</button>
      </form>
      
      </div>
    </div>
  );
};

export default PreguntaFormulario;
