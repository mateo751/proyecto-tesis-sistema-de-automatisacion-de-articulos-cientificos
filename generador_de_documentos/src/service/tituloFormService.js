// URL base del backend
const API_URL = 'http://127.0.0.1:5000';

// Función para crear un título (guarda el tema en la base de datos)
export const crearTituloForm = async (data) => {
  try {
    // Paso 1: Enviar el tema al backend y guardar en la base de datos
    const response = await fetch(`${API_URL}/tituloForm`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Error al guardar el tema en el servidor');
    }

    const responseData = await response.json();
    console.log('Tema guardado con éxito en la base de datos:', responseData);

   

  } catch (error) {
    console.error('Error en crear titulo:', error);
    throw error;
  }
};


