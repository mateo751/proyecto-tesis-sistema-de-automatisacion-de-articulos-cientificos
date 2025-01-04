import { useState } from 'react';
import { crearTitulo } from '../service/tituloService';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/GeneracionTitulo.css';



const GeneracionTitulo = () => {
  const [programaEstudio, setProgramaEstudio] = useState('');
  const [asignatura, setAsignatura] = useState('');
  const [intereses, setIntereses] = useState('');
  const [idioma, setIdioma] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [tituloResponse, setTituloResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();  // Evita que la página se recargue al enviar el formulario

    const titulo = {
      programa_de_estudio: programaEstudio,
      asignatura,
      intereses,
      idioma
    };

    try {
      const response = await crearTitulo(titulo);
      setMensaje(response.mensaje);  // Mostramos el mensaje de éxito del backend
      setTituloResponse(response.titulo_response);  // Guardamos el picoResponse en el estado
    } catch (error) {
      console.error('Error al enviar los datos', error);
      setMensaje('Error al enviar los datos');
    }
  };

  return (
    <div className="form-container">
      <div className="card-body">
      <h1 className="form-title">Título</h1>
      <p className="form-description">Generar ideas adicionales sobre el tema de un trabajo de investigación</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="studyProgram" className="form-label">Programa de estudio</label>
          <input type="text"className="form-control" value={programaEstudio} onChange={(e) => setProgramaEstudio(e.target.value)} placeholder="Ingresa el Tema a Investigar" required />
        </div>

        <div className="form-group">
          <label htmlFor="subject" className="form-label">Asignatura <span className="optional">(Opcional)</span></label>
          <input type="text"className="form-control" value={asignatura} onChange={(e) => setAsignatura(e.target.value)} placeholder="Ingresa la asignatura" required />
        </div>

        <div className="form-group">
          <label htmlFor="interests" className="form-label">Intereses <span className="optional">(Opcional)</span></label>
          <input type="text"className="form-control" value={intereses} onChange={(e) => setIntereses(e.target.value)} placeholder="Ingresa la el interes" required />
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
        {tituloResponse && (
          <div className="mt-4 text-center">
            <h3>Respuesta titulo Generada:</h3>
            {/* Si picoResponse es un array, mapea los elementos */}
            {Array.isArray(tituloResponse) ? (
              <div className="row">
                {tituloResponse.map((responseItem, index) => (
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
              <p className="card-text" >{tituloResponse}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GeneracionTitulo;
