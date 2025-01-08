// src/service/investigacionesFormService.js
const API_URL = 'http://localhost:5000';

/**
 * Prepara y valida los datos del formulario antes de enviarlos
 */
const prepareFormData = (data) => {
  const isInitialCreation = !data.query;

  const formData = {
    tema: data.tema?.trim() || '',
    pregunta_investigacion: data.pregunta_investigacion?.trim() || '',
    sub_pregunta_1: data.sub_pregunta_1?.trim() || '',
    sub_pregunta_2: data.sub_pregunta_2?.trim() || '',
    sub_pregunta_3: data.sub_pregunta_3?.trim() || '',
    anio_inicio: data.anio_inicio || 2000,
    anio_fin: data.anio_fin || 2024,
    query: data.query?.trim() || ''
  };

  // Validar campos requeridos básicos
  if (!formData.tema || !formData.pregunta_investigacion || 
      !formData.sub_pregunta_1 || !formData.sub_pregunta_2 || 
      !formData.sub_pregunta_3) {
    throw new Error('Todos los campos básicos son requeridos');
  }

  // Solo validar query si no es la creación inicial
  if (!isInitialCreation && !formData.query) {
    throw new Error('La cadena de búsqueda (query) es requerida');
  }

  return formData;
};

/**
 * Crea un nuevo formulario de investigación
 */
export const crearInvestigacionForm = async (data) => {
  try {
    console.log('Datos recibidos en el servicio:', data);

    const formData = prepareFormData(data);
    console.log('Datos preparados para enviar:', formData);

    const response = await fetch(`${API_URL}/Investigaciones/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al crear la investigación');
    }

    const responseData = await response.json();
    console.log('Respuesta del servidor:', responseData);
    return responseData;

  } catch (error) {
    console.error('Error en crearInvestigacionForm:', error);
    throw error;
  }
};

/**
 * Genera el documento de mapeo sistemático
 */
export const generarDocumentoMapeo = async (investigacionId) => {
  try {
    console.log('Generando documento para ID:', investigacionId);

    const response = await fetch(`${API_URL}/Investigaciones/${investigacionId}/mapping-document`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al generar el documento');
    }

    const documentData = await response.json();
    console.log('Documento generado:', documentData);
    return documentData;

  } catch (error) {
    console.error('Error en generarDocumentoMapeo:', error);
    throw error;
  }
};

/**
 * Actualiza el documento de mapeo sistemático
 */
export const actualizarDocumentoMapeo = async (investigacionId) => {
  try {
    console.log('Actualizando documento para ID:', investigacionId);

    const response = await fetch(`${API_URL}/Investigaciones/${investigacionId}/mapping-document`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al actualizar el documento');
    }

    const documentData = await response.json();
    console.log('Documento actualizado:', documentData);
    return documentData;

  } catch (error) {
    console.error('Error en actualizarDocumentoMapeo:', error);
    throw error;
  }
};

/**
 * Obtiene el documento de mapeo existente
 */
export const obtenerDocumentoMapeo = async (investigacionId) => {
  try {
    const response = await fetch(`${API_URL}/Investigaciones/${investigacionId}/document`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al obtener el documento');
    }

    const documentData = await response.json();
    return documentData;

  } catch (error) {
    console.error('Error en obtenerDocumentoMapeo:', error);
    throw error;
  }
};