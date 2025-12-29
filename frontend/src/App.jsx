import React, { useState, useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Layout from './components/Layout/Layout';
import Sidebar, { SidebarTab } from './components/Layout/Sidebar';
import MapComponent from './components/Map/Map';
import LayerList from './components/Layers/LayerList';
import FileUpload from './components/Upload/FileUpload';
import SpatialQuery from './components/Query/SpatialQuery';
import queryService from './services/queryService';
import layerService from './services/layerService';
import { toast } from 'react-toastify';
import './App.css';

function App() {
  const [mapLayers, setMapLayers] = useState([]);
  const [queryResults, setQueryResults] = useState(null);

  useEffect(() => {
    // Load initial data
    loadInitialLayers();
  }, []);

  const loadInitialLayers = async () => {
    try {
      // Load Vietnam cities
      await loadVietnamCities();
      // Load highways
      await loadHighways();
    } catch (error) {
      console.error('Error loading initial layers:', error);
    }
  };

  const loadVietnamCities = async () => {
    try {
      const results = await queryService.queryBBox('vietnam_cities', [
        102.0, 8.0, 110.0, 24.0
      ]);
      if (results && results.features) {
        setMapLayers((prev) => [
          ...prev.filter((l) => l.name !== 'vietnam_cities'),
          {
            name: 'vietnam_cities',
            type: 'vector',
            features: results.features,
            visible: true,
            opacity: 1.0,
          },
        ]);
      }
    } catch (error) {
      console.error('Error loading Vietnam cities:', error);
    }
  };

  const loadHighways = async () => {
    try {
      const highways = await layerService.getHighways();
      if (highways && highways.length > 0) {
        // Convert highways to GeoJSON features
        const features = highways.map((highway) => ({
          type: 'Feature',
          geometry: highway.geometry,
          properties: {
            id: highway.id,
            name: highway.name,
            name_en: highway.name_en,
            type: highway.type,
            length_km: highway.length_km,
            lanes: highway.lanes,
            max_speed: highway.max_speed,
            status: highway.status,
            start_point: highway.start_point,
            end_point: highway.end_point,
            opened_date: highway.opened_date,
            description: highway.description,
          },
        }));

        setMapLayers((prev) => [
          ...prev.filter((l) => l.name !== 'highways'),
          {
            name: 'highways',
            type: 'vector',
            features: features,
            visible: true,
            opacity: 1.0,
            style: 'highway',
          },
        ]);
      }
    } catch (error) {
      console.error('Error loading highways:', error);
    }
  };

  const handleLayersChange = (layers) => {
    // Convert layer metadata to map layers
    // For now, just update visibility and opacity
    console.log('Layers changed:', layers);
  };

  const handleUploadSuccess = (result) => {
    toast.success('Upload successful! Reloading map...');
    // Reload the layer
    setTimeout(() => {
      loadInitialLayers();
    }, 1000);
  };

  const handleQueryResults = (results) => {
    setQueryResults(results);
    if (results && results.features) {
      // Add query results as a temporary layer
      setMapLayers((prev) => [
        ...prev.filter((l) => l.name !== 'query_results'),
        {
          name: 'query_results',
          type: 'vector',
          features: results.features,
          visible: true,
          opacity: 1.0,
        },
      ]);
    }
  };

  const handleFeatureClick = (featureInfo) => {
    console.log('Feature clicked:', featureInfo);
    const props = featureInfo.properties;
    let message = 'Feature Info:\n';
    Object.keys(props).forEach((key) => {
      if (key !== 'geometry' && key !== 'geom') {
        message += `${key}: ${props[key]}\n`;
      }
    });
    toast.info(message, { autoClose: 5000 });
  };

  return (
    <Layout>
      <Sidebar>
        <SidebarTab tabId="layers">
          <LayerList onLayersChange={handleLayersChange} />
        </SidebarTab>
        <SidebarTab tabId="upload">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </SidebarTab>
        <SidebarTab tabId="query">
          <SpatialQuery onQueryResults={handleQueryResults} />
        </SidebarTab>
      </Sidebar>
      <div className="map-container-wrapper">
        <MapComponent layers={mapLayers} onFeatureClick={handleFeatureClick} />
      </div>
      <ToastContainer position="bottom-right" autoClose={3000} />
    </Layout>
  );
}

export default App;
