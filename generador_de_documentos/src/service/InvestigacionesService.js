// Aquí definimos la URL base del backend. Cámbiala si es necesario.
const API_URL = 'http://127.0.0.1:5000/investigaciones';  // Asegúrate de que el puerto sea el correcto

export const crearInvestigaciones = async (data) => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',  // Método POST para enviar los datos
      headers: {
        'Content-Type': 'application/json',  // Asegúrate de que se está enviando como JSON
      },
      body: JSON.stringify(data),  // Convierte los datos a JSON
    });

    if (!response.ok) {
      // Si la respuesta no es "ok", lanzamos un error
      throw new Error('Error en la solicitud al servidor');
    }

    const responseData = await response.json();  // Convertimos la respuesta a JSON
    return responseData;  // Devolvemos los datos
  } catch (error) {
    console.error('Error en crear Investigacion:', error);
    throw error;  // Relanzamos el error para que lo maneje el componente
  }
};