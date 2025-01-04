import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/BuscarFuentes.css'; // Asegúrate de tener el archivo CSS correspondiente

const BuscarFuentes = () => {
  const [cadenaBusqueda, setCadenaBusqueda] = useState('');
  const [accesoAbierto, setAccesoAbierto] = useState(false);
  const [anioInicio, setAnioInicio] = useState(1964); // Año inicial del rango
  const [anioFin, setAnioFin] = useState(1981); // Año final del rango
  const [idioma, setIdioma] = useState('us en');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/create/seleccionFuentesForm');
    // Validación simple: el año de inicio no puede ser mayor que el año de fin
    if (anioInicio > anioFin) {
      alert('El año de inicio no puede ser mayor que el año de fin.');
      return;
    }
    // Aquí iría la lógica para manejar la búsqueda
    console.log({
      cadenaBusqueda,
      accesoAbierto,
      anioInicio,
      anioFin,
      idioma,
    });
  };

  return (
    <div className="form-container">
      <div className="card-body">
        <h1 className="form-title">Buscar fuentes</h1>
        <p className="form-description">
          Búsqueda de fuentes académicas que puedan ser relevantes para el tema.
        </p>

        <form onSubmit={handleSubmit}>
          {/* cadena de busqueda */}
          <div className="mb-3">
          <label className="form-label">Cadena de busqueda</label>
          <select
              className="form-control"
              value={cadenaBusqueda}
              onChange={(e) => setCadenaBusqueda(e.target.value)}
            >
              <option value="us en">cadenaBusqueda</option>
              {/* Agrega más opciones si es necesario */}
            </select>
          </div>

          {/* Acceso abierto */}
          <div className="mb-3">
            <label className="form-label">
              Acceso abierto <span className="optional">(opcional)</span>
            </label>
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
                min="1900"
                max="2024"
                value={anioInicio}
                onChange={(e) => setAnioInicio(parseInt(e.target.value, 10))}
              />
              <input
                type="range"
                className="slider"
                min="1900"
                max="2024"
                value={anioFin}
                onChange={(e) => setAnioFin(parseInt(e.target.value, 10))}
              />
            </div>
          </div>

          {/* Idioma */}
          <div className="mb-3">
            <label className="form-label">
              Idioma <span className="optional">(opcional)</span>
            </label>
            <select
              className="form-control"
              value={idioma}
              onChange={(e) => setIdioma(e.target.value)}
            >
              <option value="us en">US-en</option>
              <option value="es es">ES-es</option>
              {/* Agrega más opciones si es necesario */}
            </select>
          </div>

          {/* Botón de enviar */}
          <button type="submit" className="btn-submit">
            generar
          </button>
        </form>
      </div>
    </div>
  );
};

export default BuscarFuentes;
