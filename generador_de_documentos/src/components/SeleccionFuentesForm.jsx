import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function DocumentSelection() {
  // Ejemplo de datos para los artículos
  const documents = [
    {
      title: 'Sistema de reconocimiento facial para el control de acceso mediante Inteligencia Artificial',
      description: 'El presente artículo tiene como objetivo principal el desarrollo de un sistema que permita el reconocimiento facial de una persona para el control de acceso mediante Inteligencia Artificial.',
      authors: 'Campos, J. E. R. P., Rodriguez, C.S.C., Luján, L.D.A., Santos, A. C. M. de los',
      year: 2023,
    },
    {
      title: 'Procesamiento De Imágenes Para La Identificación De Personas Como Sistema De Seguridad En Zonas Domiciliarias',
      description: 'Image Processing for identification of people as a security system in domiciliary zones.',
      authors: 'Granja, I., Moreno, D., Cabrera, F., Valle, P.',
      year: 2020,
    },
  ];
  const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        navigate('/investigaciones');  // Evita que la página se recargue al enviar el formulario
    };
  return (
    <div className="container my-4">
      <h1 className="text-center">Selección de artículos</h1>
      <p className="text-center">Selecciona los mejores documentos que puedan ser relevantes para el tema.</p>
      
      <div className="d-flex justify-content-end">
        <button className="btn btn-light mb-3">+ Generar extracción de datos</button>
      </div>
      <form onSubmit={handleSubmit}>
      <div className="document-list">
        {documents.map((doc, index) => (
          <div key={index} className="card mb-3 shadow-sm">
            <div className="card-body">
              <div>
                  <span className="text-muted">borrar</span>
              </div>
              <h5 className="card-title">{doc.title}</h5>
              <p className="card-text">{doc.description}</p>
              <p className="card-text">
                <small className="text-muted">{doc.authors}, {doc.year}</small>
              </p>
              
              <div className="d-flex justify-content-between">
                <div>
                  <a href="#" className="text-decoration-none me-3">direct pdf access</a>
                  <a href="#" className="text-decoration-none">source info</a>
                </div>
                
              </div>
            </div>
          </div>
        ))}
      </div>
      
      
        <button className="btn btn-dark">Generar documento</button>
        </form>
      
    </div>
  );
}

export default DocumentSelection;
