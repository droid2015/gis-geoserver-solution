export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const GEOSERVER_URL = process.env.REACT_APP_GEOSERVER_URL || 'http://localhost:8080/geoserver';

export const MAP_CENTER = [
  parseFloat(process.env.REACT_APP_MAP_CENTER_LON) || 106.0,
  parseFloat(process.env.REACT_APP_MAP_CENTER_LAT) || 16.0,
];

export const MAP_ZOOM = parseInt(process.env.REACT_APP_MAP_ZOOM) || 12;

export const DRAW_TYPES = {
  POINT: 'Point',
  LINE: 'LineString',
  POLYGON: 'Polygon',
  BOX: 'Box',
};

export const QUERY_TYPES = {
  BBOX: 'bbox',
  INTERSECT: 'intersect',
  BUFFER: 'buffer',
  WITHIN: 'within',
};

export const FILE_TYPES = {
  SHAPEFILE: 'shapefile',
  GEOJSON: 'geojson',
};
