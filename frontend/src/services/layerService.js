import api from './api';

export const layerService = {
  // Get all layers
  getLayers: async () => {
    const response = await api.get('/api/layers');
    return response.data;
  },

  // Get layer by ID
  getLayer: async (id) => {
    const response = await api.get(`/api/layers/${id}`);
    return response.data;
  },

  // Create new layer
  createLayer: async (layerData) => {
    const response = await api.post('/api/layers', layerData);
    return response.data;
  },

  // Update layer
  updateLayer: async (id, layerData) => {
    const response = await api.put(`/api/layers/${id}`, layerData);
    return response.data;
  },

  // Delete layer
  deleteLayer: async (id) => {
    const response = await api.delete(`/api/layers/${id}`);
    return response.data;
  },

  // Get highways
  getHighways: async () => {
    const response = await api.get('/api/layers/highways');
    return response.data;
  },
};

export default layerService;
