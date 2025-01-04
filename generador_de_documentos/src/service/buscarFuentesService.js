// Define la URL base del backend. Cambia el puerto o la ruta si es necesario.
const API_URL_SCOPUS = 'http://127.0.0.1:5000/encontrar-fuentes';

export const buscarFuentes = async (data) => {
  try {
    const response = await fetch(API_URL_SCOPUS, {
      method: 'POST',  // Método POST
      headers: {
        'Content-Type': 'application/json',  // Enviamos JSON
      },
      body: JSON.stringify(data),  // Convertimos los datos a JSON
    });

    if (!response.ok) {
      // Si la respuesta no es "ok", lanzamos un error
      throw new Error('Error al realizar la búsqueda en Scopus');
    }

    const responseData = await response.json();  // Convertimos la respuesta a JSON
    return responseData;  // Devolvemos los datos de la respuesta
  } catch (error) {
    console.error('Error en buscarFuentes:', error);
    throw error;  // Relanzamos el error para manejarlo en el componente
  }
};
