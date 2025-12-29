import api from './api';

export const uploadService = {
  // Upload shapefile
  uploadShapefile: async (file, layerName, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('layer_name', layerName);

    const response = await api.post('/api/upload/shapefile', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });
    return response.data;
  },

  // Upload GeoJSON
  uploadGeoJSON: async (file, layerName, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('layer_name', layerName);

    const response = await api.post('/api/upload/geojson', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });
    return response.data;
  },

  // Get upload status
  getUploadStatus: async (taskId) => {
    const response = await api.get(`/api/upload/status/${taskId}`);
    return response.data;
  },
};

export default uploadService;
