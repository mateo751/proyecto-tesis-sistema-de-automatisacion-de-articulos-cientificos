import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import GeneracionMetodoPICO from './components/GeneracionMetodoPICO';
import GeneracionTitulo from './components/GeneracionTitulo';
import Investigaciones from './components/Investigaciones';
import BuscarFuentes from './components/BuscarFuentes';
import GeneracionPreguntas from './components/GeneracionPreguntas';
import VistaPrincipal from './components/VistaPrincipal' // Importa el nuevo componente
import SeleccionFuentesForm from './components/SeleccionFuentesForm'
import InvetigacionesForm  from './components/investigacionesForm'

import 'bootstrap/dist/css/bootstrap.min.css';
import './components/css/VistaPrincipal.css';  // Estilos globales

const App = () => {
  return (
    <Router>
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-3 col-lg-2 bg-light">
            <nav className="position-sticky">
              <ul className="nav flex-column">
                <li className="nav-item">
                  <h4 className="text-center">Mapping Studying</h4>
                </li>
                <li className="nav-item">
                  <Link to="/Investigaciones" className="nav-link">Mis Investigaciones</Link>
                </li>
                <li className="nav-item">
                  <Link to="/titulo" className="nav-link">Título</Link>
                </li>
                <li className="nav-item">
                  <Link to="/preguntas" className="nav-link">Preguntas de Investigacion</Link>
                </li>
                <li className="nav-item">
                  <Link to="/metodo-pico" className="nav-link">Generacion de metodo PICO</Link>
                </li>
                <li className="nav-item">
                  <Link to="/encontrar-fuentes" className="nav-link">Encontrar Fuentes</Link>
                </li>
                <li className="nav-item">
                  <Link to="/extraccion-datos" className="nav-link">Generar Matriz de Extraccion de Datos</Link>
                </li>
              </ul>
            </nav>
          </div>

          {/* Contenido principal */}
          <div className="col-md-9 col-lg-10">
        
            <Routes>
              {/* Nueva ruta para la vista de bienvenida */}
              <Route path="/" element={<VistaPrincipal/>} /> {/* Ruta por defecto */}

              {/* Rutas existentes */}
              <Route path="/Investigaciones" element={<Investigaciones />} />
              <Route path="/Investigaciones/create" element={<InvetigacionesForm />} />
              <Route path="/titulo" element={<GeneracionTitulo />} />
              <Route path="/preguntas" element={<GeneracionPreguntas />} />
              <Route path="/metodo-pico" element={<GeneracionMetodoPICO />} />
              <Route path="/encontrar-fuentes" element={<BuscarFuentes />} />
              <Route path="/extraccion-datos" element={<SeleccionFuentesForm/>} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;
