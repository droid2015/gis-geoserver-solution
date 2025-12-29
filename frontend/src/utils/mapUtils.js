import { fromLonLat, toLonLat } from 'ol/proj';
import { boundingExtent } from 'ol/extent';

export const transformCoordinates = (coordinates, fromProj = 'EPSG:4326', toProj = 'EPSG:3857') => {
  if (Array.isArray(coordinates[0])) {
    return coordinates.map((coord) => transformCoordinates(coord, fromProj, toProj));
  }
  return fromLonLat ? fromLonLat(coordinates) : coordinates;
};

export const getExtentFromBBox = (bbox) => {
  return boundingExtent([
    fromLonLat([bbox[0], bbox[1]]),
    fromLonLat([bbox[2], bbox[3]]),
  ]);
};

export const formatCoordinate = (coordinate) => {
  const lonLat = toLonLat(coordinate);
  return `${lonLat[1].toFixed(4)}°, ${lonLat[0].toFixed(4)}°`;
};

export const createWMSLayer = (url, workspace, layerName) => {
  return `${url}/${workspace}/wms`;
};

export const createWFSUrl = (url, workspace, layerName) => {
  return `${url}/${workspace}/wfs`;
};
