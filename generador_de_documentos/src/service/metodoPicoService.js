// Aquí definimos la URL base del backend. Cámbiala si es necesario.
const API_URL = 'http://127.0.0.1:5000/metodoPico';  // Asegúrate de que el puerto sea el correcto

export const crearMetodoPico = async (data) => {
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
    console.log('Datos recibidos del backend:', responseData);

    // Si 'pico_response' no existe, establecer un valor por defecto
    const picoResponse = responseData.pico_response || 'No se generó un PICO response';
    
    return {
      mensaje: responseData.mensaje,
      id: responseData.id,
      pico_response: picoResponse  // Siempre devolver un valor para 'pico_response'
    };
  } catch (error) {
    console.error('Error en crear MetodoPico:', error);
    throw error;  // Relanzamos el error para que lo maneje el componente
  }
};
