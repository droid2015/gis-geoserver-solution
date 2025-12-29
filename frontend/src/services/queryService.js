import api from './api';

export const queryService = {
  // Bounding box query
  queryBBox: async (layerName, bbox) => {
    const response = await api.post('/api/query/bbox', {
      layer_name: layerName,
      minx: bbox[0],
      miny: bbox[1],
      maxx: bbox[2],
      maxy: bbox[3],
      srid: 4326,
    });
    return response.data;
  },

  // Intersection query
  queryIntersect: async (layerName, geometry) => {
    const response = await api.post('/api/query/intersect', {
      layer_name: layerName,
      geometry: geometry,
      srid: 4326,
    });
    return response.data;
  },

  // Buffer query
  queryBuffer: async (layerName, geometry, distance) => {
    const response = await api.post('/api/query/buffer', {
      layer_name: layerName,
      geometry: geometry,
      distance: distance,
      srid: 4326,
    });
    return response.data;
  },

  // Within query
  queryWithin: async (layerName, geometry) => {
    const response = await api.post('/api/query/within', {
      layer_name: layerName,
      geometry: geometry,
      srid: 4326,
    });
    return response.data;
  },

  // Get layer attributes
  getAttributes: async (layerName) => {
    const response = await api.get(`/api/query/attributes/${layerName}`);
    return response.data;
  },
};

export default queryService;
