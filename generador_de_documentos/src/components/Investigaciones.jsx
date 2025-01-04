import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importamos useNavigate
import './css/Investigaciones.css';

const MisInvestigaciones = () => {
  const [showModal, setShowModal] = useState(false);
  const [data, setData] = useState([]); // Estado para almacenar los datos de la tabla
  const [newData, setNewData] = useState({ nombre: '', tipo: '' }); // Estado para el formulario

  const navigate = useNavigate(); // Inicializamos el hook de navegación

  // Función para manejar la apertura/cierre del modal
  const toggleModal = () => {
    setShowModal(!showModal);
  };

  // Función para generar la fecha actual en formato YYYY-MM-DD
  const getCurrentDate = () => {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Mes con dos dígitos
    const dd = String(today.getDate()).padStart(2, '0'); // Día con dos dígitos
    return `${yyyy}-${mm}-${dd}`;
  };

  // Función para manejar el envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault();

    // Agregar el nuevo dato con la fecha actual
    setData([...data, { ...newData, fecha: getCurrentDate() }]);

    toggleModal(); // Cierra el modal
    setNewData({ nombre: '', tipo: '' }); // Resetea el formulario
  };

  // Función para manejar la redirección al generar documento
  const handleGenerarDocumento = () => {
    navigate('/Investigaciones/create'); // Navega a la vista de generación de documento
  };

  return (
    <div className="fuentes-container">
      <div className="header">
        <h1 className="title">Mis Investigaciones</h1>
        <button className="btn btn-outline-dark nuevo-doc-btn" onClick={handleGenerarDocumento}>
          + Nuevo documento
        </button>
      </div>

      {/* Tabla de datos */}
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Creado en ▼</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((item, index) => (
              <tr key={index}>
                <td>{item.nombre}</td>
                <td>{item.fecha}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="no-data">No hay datos disponibles</td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Contenedor para botón y paginación */}
      <div className="table-footer">
        <div className="pagination-controls">
          <span>Filas por página:</span>
          <select className="rows-per-page">
            <option value="15">15</option>
            <option value="30">30</option>
            <option value="50">50</option>
          </select>
          <span> 1 - 0 de 0 </span>
          <button className="btn btn-link disabled pagination-btn">‹</button>
          <button className="btn btn-link disabled pagination-btn">›</button>
        </div>

        
      </div>

      {/* Modal para agregar nuevo documento */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button className="close-btn" onClick={toggleModal}>X</button>
            <h2>Nuevo documento</h2>
            <form onSubmit={handleSubmit}>
              <div>
                <label>Nombre del Documento:</label>
                <input
                  type="text"
                  value={newData.nombre}
                  onChange={(e) => setNewData({ ...newData, nombre: e.target.value })}
                  required
                />
              </div>
              <div>
                <label>Tipo de Investigaciones:</label>
                <input
                  type="text"
                  value={newData.tipo}
                  onChange={(e) => setNewData({ ...newData, tipo: e.target.value })}
                  required
                />
              </div>
              <button type="submit">Añadir</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MisInvestigaciones;
