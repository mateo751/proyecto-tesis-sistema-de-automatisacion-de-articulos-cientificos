import { Link } from 'react-router-dom';
import './css/VistaPrincipal.css'; // Si quieres agregar estilos específicos.

const WelcomeView = () => {
  return (
    <div className="welcome-container">
      <h1 className="welcome-title">Welcome to Projects</h1>
      <p className="welcome-description">
      Los proyectos son una forma de organizar la investigación y la escritura. Al crear un proyecto, 
      puedes mantener el contexto de tu escritura coherente y crear textos más rápidamente.
      </p>
      <div className="welcome-action">
        <Link to="/investigaciones" className="btn btn-dark btn-lg">Create First Project</Link>
      </div>
    </div>
  );
};

export default WelcomeView;
