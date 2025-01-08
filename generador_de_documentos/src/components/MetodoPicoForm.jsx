import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
//import { crearMetodoPico } from '../service/';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionMetodoPICO.css';

const GeneracionMetodoPICO = () => {
  const [preguntaInvestigacion, setPreguntaInvestigacion] = useState('');
  const [subPregunta1, setSubPregunta1] = useState('');
  const [subPregunta2, setSubPregunta2] = useState('');
  const [subPregunta3, setSubPregunta3] = useState('');
  const navigate = useNavigate();
 // Estado para almacenar el picoResponse

  const handleSubmit = async (e) => {
    e.preventDefault();
    navigate('/Investigaciones/create');  // Evita que la página se recargue al enviar el formulario
  };

  return (
    <div className="form-container">
      <div className="card-body">
        <h1 className="form-title">Datos informativos del artículo</h1>
        <p className="form-description">Buscar palabras clave sobre el trabajo de investigación</p>
        <form onSubmit={handleSubmit}>
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
      </div>
    </div>
  );
};

export default GeneracionMetodoPICO;
