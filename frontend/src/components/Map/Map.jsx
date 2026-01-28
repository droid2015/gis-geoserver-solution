import React, { useEffect, useRef, useState } from 'react';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import { defaults as defaultControls, ScaleLine, FullScreen, MousePosition } from 'ol/control';
import { format } from 'ol/coordinate';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
import './Map.css';
import { MAP_CENTER, MAP_ZOOM } from '../../utils/constants';

const MapComponent = ({ layers, onFeatureClick }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const [mapReady, setMapReady] = useState(false);

  useEffect(() => {
    if (!mapRef.current) return;

    // Create base layer
    const baseLayer = new TileLayer({
      source: new OSM(),
      properties: { name: 'OSM Base Map' },
    });

    // Mouse position control
    const mousePositionControl = new MousePosition({
      coordinateFormat: (coord) => format(coord, '{y}, {x}', 4),
      projection: 'EPSG:4326',
      className: 'custom-mouse-position',
      target: document.getElementById('mouse-position'),
    });

    // Initialize map
    const map = new Map({
      target: mapRef.current,
      layers: [baseLayer],
      view: new View({
        center: fromLonLat(MAP_CENTER),
        zoom: MAP_ZOOM,
      }),
      controls: defaultControls().extend([
        new ScaleLine(),
        new FullScreen(),
        mousePositionControl,
      ]),
    });

    // Handle feature click
    map.on('click', (evt) => {
      const features = [];
      map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
        features.push({
          feature,
          layer,
          properties: feature.getProperties(),
        });
      });

      if (features.length > 0 && onFeatureClick) {
        onFeatureClick(features[0]);
      }
    });

    mapInstanceRef.current = map;
    setMapReady(true);

    return () => {
      map.setTarget(null);
    };
  }, [onFeatureClick]);

  // Update layers
  useEffect(() => {
    if (!mapReady || !mapInstanceRef.current) return;

    const map = mapInstanceRef.current;
    const currentLayers = map.getLayers().getArray();

    // Remove all non-base layers
    currentLayers.forEach((layer, index) => {
      if (index > 0) {
        map.removeLayer(layer);
      }
    });

    // Add new layers
    layers.forEach((layerConfig) => {
      if (!layerConfig.visible) return;

      // GeoServer WMS Layer
      if (layerConfig.type === 'wms') {
        const wmsLayer = new TileLayer({
          source: new TileWMS({
            url: layerConfig.url || 'http://localhost:8080/geoserver/wms',
            params: {
              'LAYERS': layerConfig.layers,
              'TILED': true,
              'VERSION': '1.1.0'
            },
            serverType: 'geoserver',
            crossOrigin: 'anonymous'
          }),
          opacity: layerConfig.opacity || 1.0,
          properties: { name: layerConfig.name }
        });
        map.addLayer(wmsLayer);
      }
      // Vector Layer
      else if (layerConfig.type === 'vector' && layerConfig.features) {
        const vectorSource = new VectorSource({
          features: new GeoJSON().readFeatures(
            {
              type: 'FeatureCollection',
              features: layerConfig.features,
            },
            {
              featureProjection: 'EPSG:3857',
            }
          ),
        });

        // Define style based on layer type
        let layerStyle;
        if (layerConfig.style === 'highway' || layerConfig.name === 'highways') {
          // Highway style - orange line
          layerStyle = new Style({
            stroke: new Stroke({
              color: '#FF6B00',
              width: 4,
              lineCap: 'round'
            }),
          });
        } else {
          // Default style - for points and polygons
          layerStyle = new Style({
            image: new CircleStyle({
              radius: 6,
              fill: new Fill({ color: '#3399CC' }),
              stroke: new Stroke({ color: '#fff', width: 2 }),
            }),
            fill: new Fill({ color: 'rgba(51, 153, 204, 0.2)' }),
            stroke: new Stroke({ color: '#3399CC', width: 2 }),
          });
        }

        const vectorLayer = new VectorLayer({
          source: vectorSource,
          style: layerStyle,
          opacity: layerConfig.opacity || 1.0,
          properties: { name: layerConfig.name },
        });

        map.addLayer(vectorLayer);
      }
    });
  }, [layers, mapReady]);

  return (
    <div className="map-container">
      <div ref={mapRef} className="map" />
      <div id="mouse-position" className="mouse-position" />
    </div>
  );
};

export default MapComponent;
