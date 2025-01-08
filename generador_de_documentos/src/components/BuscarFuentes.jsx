import { useState } from 'react';
import { buscarFuentes } from '../service/buscarFuentesService'; // Importa el servicio
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/BuscarFuentes.css';

const BuscarFuentes = () => {
  const [tema, setTema] = useState('');
  const [accesoAbierto, setAccesoAbierto] = useState(false);
  const [anioInicio, setAnioInicio] = useState(1964);
  const [anioFin, setAnioFin] = useState(1981);
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (anioInicio > anioFin) {
      alert('El año de inicio no puede ser mayor que el año de fin.');
      return;
    }

    setLoading(true);
    setError(null);

    // Construimos el payload para la solicitud
    const payload = {
      query: tema,
      count: 10, // Puedes ajustar este valor según sea necesario
    };

    try {
      // Llamamos al servicio para buscar fuentes
      const response = await buscarFuentes(payload);
      setResultados(response.resultados); // Guardamos los resultados en el estado
    } catch (err) {
      console.error(err);
      setError('Hubo un error al realizar la búsqueda. Inténtalo nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <div className="card-body">
        <h1 className="form-title">Buscar fuentes</h1>
        <p className="form-description">
          Búsqueda de fuentes académicas relevantes para el tema.
        </p>

        <form onSubmit={handleSubmit}>
          {/* Tema */}
          <div className="mb-3">
            <label className="form-label">Tema</label>
            <input
              type="text"
              className="form-control"
              value={tema}
              onChange={(e) => setTema(e.target.value)}
              placeholder="Ciencia de la Computación"
              required
            />
          </div>

          {/* Acceso abierto */}
          <div className="mb-3">
            <label className="form-label">Acceso abierto (opcional)</label>
            <div className="checkbox-container">
              <input
                type="checkbox"
                id="accesoAbierto"
                checked={accesoAbierto}
                onChange={() => setAccesoAbierto(!accesoAbierto)}
              />
              <label htmlFor="accesoAbierto">
                Mostrar solo fuentes de acceso abierto
              </label>
            </div>
          </div>

          {/* Año de publicación */}
          <div className="mb-3">
            <label className="form-label">Año de publicación</label>
            <div className="range-slider">
              <div className="slider-labels">
                <span>{anioInicio}</span>
                <span>{anioFin}</span>
              </div>
              <input
                type="range"
                className="slider"
                min="2000"
                max="2024"
                value={anioInicio}
                onChange={(e) => setAnioInicio(parseInt(e.target.value, 10))}
              />
              <input
                type="range"
                className="slider"
                min="2000"
                max="2024"
                value={anioFin}
                onChange={(e) => setAnioFin(parseInt(e.target.value, 10))}
              />
            </div>
          </div>

          {/* Botón de enviar */}
          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Cargando...' : 'Generar'}
          </button>
         
        </form>

        {/* Mostrar resultados */}
        {error && <p className="error-message">{error}</p>}
        {resultados.length > 0 && (
          <div className="container my-4">
            <h1 className="text-center">Selección de artículos</h1>
            <p className="text-center">Selecciona los mejores documentos que puedan ser relevantes para el tema.</p>
            <div className="d-flex justify-content-end">
            <button className="btn btn-light mb-3">+ Generar extracción de datos</button>
            </div>
            <div className="document-list">
            
            
              {resultados.map((resultado, index) => (
                <div key={index} className="card mb-3 shadow-sm">
                <div className="card-body">
                <div>
                  <span className="text-muted">borrar</span>
                </div>

          
                  <h3 className="card-title">{resultado.title}</h3>
                  <p className="card-text"><strong>Autores:</strong> {resultado.authors}</p>
                  <p className="card-text"><strong>Revista:</strong> {resultado.journal}</p>
                  <p className="card-text"><strong>Fecha de publicación:</strong> {resultado.publication_date}</p>
                  {resultado.doi && (
                    <p>
                      <strong>DOI:</strong>{' '}
                      <a href={`https://doi.org/${resultado.doi}`} className="text-decoration-none me-3" target="_blank" rel="noopener noreferrer">
                        {resultado.doi}
                      </a>
                    </p>
                  )}
           
                </div>
               </div> 
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuscarFuentes;
