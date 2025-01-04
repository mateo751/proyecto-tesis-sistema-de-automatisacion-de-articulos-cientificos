import { useState } from "react";
import { useNavigate } from 'react-router-dom';

import './css/TituloFormulario.css';

const TituloFormulario = () => {
  const [tema, setTema] = useState("");
  const navigate = useNavigate();


  const handleSubmit = (e) => {
    e.preventDefault();

    navigate('/Investigaciones/create');  // Navegar al siguiente paso
  };

  return (
    <div className="form-container">
      <h2>Su tema</h2>
      <p>Escriba su tema o idea...</p>
      <form onSubmit={handleSubmit}>
        <textarea
          value={tema}
          onChange={(e) => setTema(e.target.value)}
          placeholder="Ingresa tu tema aquí"
          className="tema-textarea"
        />
        <button type="submit" disabled={!tema} className={`submit-button ${!tema ? 'disabled' : ''}`}>
          Próximo
        </button>
      </form>
    </div>
  );
};

export default TituloFormulario;
