import api from './api';

export const geoserverService = {
  // Get workspaces
  getWorkspaces: async () => {
    const response = await api.get('/api/geoserver/workspaces');
    return response.data;
  },

  // Create workspace
  createWorkspace: async (name) => {
    const response = await api.post(`/api/geoserver/workspaces?workspace_name=${name}`);
    return response.data;
  },

  // Get layers
  getLayers: async (workspace = null) => {
    const url = workspace
      ? `/api/geoserver/layers?workspace=${workspace}`
      : '/api/geoserver/layers';
    const response = await api.get(url);
    return response.data;
  },

  // Publish layer
  publishLayer: async (workspace, datastore, tableName, title) => {
    const response = await api.post('/api/geoserver/publish', null, {
      params: {
        workspace,
        datastore,
        table_name: tableName,
        title,
      },
    });
    return response.data;
  },

  // Delete layer
  deleteLayer: async (workspace, layerName) => {
    const response = await api.delete(`/api/geoserver/layers/${workspace}/${layerName}`);
    return response.data;
  },

  // Get styles
  getStyles: async () => {
    const response = await api.get('/api/geoserver/styles');
    return response.data;
  },
};

export default geoserverService;
