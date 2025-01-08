import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import './css/GeneracionMetodoPICO.css'; // Opcional si deseas añadir estilos personalizados

const EvaluacionMetodoPico = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const navigate = useNavigate();
  const anterior = useNavigate();

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Aquí podrías agregar la lógica para manejar el envío del formulario
    console.log('Tema seleccionado:', selectedOption);
  };
  const handleProximoClick = () => {
    navigate('/create/metodoPicoForm'); // Redirige a la vista TemaEvaluacion
  };
  const handleAnteriorClick = () => {
    anterior('/create/buscarFuentesForm'); // Redirige a la vista TemaEvaluacion
  };
  return (
    <div className="evaluacion-container">
      <h1>Su cadena  de busqueda </h1>
      <p className="evaluacion-description">Evalua las palabras claves que puedan tener mejor impacto en la investigacion</p>
      <p className="tema-evaluacion-aviso">
        Aqui ban palabras claves que se generan en el metodo pico 
      </p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="input-tema"
          placeholder="Escribe tu tema aquí"
          value={selectedOption}
          onChange={handleOptionChange}
        />

        <div className="opciones-tema">
          <label className="opcion">
            <input
              type="radio"
              value="cadena generada uno"
              checked={selectedOption === 'cadena generada uno'}
              onChange={handleOptionChange}
            />
            cadena generada uno
          </label>

          <label className="opcion">
            <input
              type="radio"
              value="cadena generada dos"
              checked={selectedOption === 'cadena generada dos'}
              onChange={handleOptionChange}
            />
            cadena generada dos
          </label>

          <label className="opcion">
            <input
              type="radio"
              value="cadena generada tres"
              checked={selectedOption === 'cadena generada tres'}
              onChange={handleOptionChange}
            />
            cadena generada tres
          </label>
        </div>

        <button type="submit" className="btn btn-dark btn-lg mt-3" onClick={handleProximoClick}>Anterior</button>
        <button type="submit" className="btn btn-dark btn-lg mt-3" onClick={handleAnteriorClick}>Próximo</button>
      </form>
    </div>
  );
};

export default EvaluacionMetodoPico;
