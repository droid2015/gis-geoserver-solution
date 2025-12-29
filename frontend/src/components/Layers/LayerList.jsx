import React, { useEffect, useState } from 'react';
import layerService from '../../services/layerService';
import geoserverService from '../../services/geoserverService';
import { toast } from 'react-toastify';
import './LayerList.css';

const LayerList = ({ onLayersChange }) => {
  const [layers, setLayers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLayers();
  }, []);

  const loadLayers = async () => {
    setLoading(true);
    try {
      const data = await layerService.getLayers();
      setLayers(data);
      if (onLayersChange) {
        onLayersChange(data);
      }
    } catch (error) {
      toast.error('Error loading layers: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVisibilityToggle = async (layer) => {
    try {
      const updated = await layerService.updateLayer(layer.id, {
        visible: !layer.visible,
      });
      setLayers((prev) =>
        prev.map((l) => (l.id === layer.id ? updated : l))
      );
      if (onLayersChange) {
        onLayersChange(layers.map((l) => (l.id === layer.id ? updated : l)));
      }
      toast.success('Layer visibility updated');
    } catch (error) {
      toast.error('Error updating layer: ' + error.message);
    }
  };

  const handleOpacityChange = async (layer, opacity) => {
    try {
      const updated = await layerService.updateLayer(layer.id, {
        opacity: parseFloat(opacity),
      });
      setLayers((prev) =>
        prev.map((l) => (l.id === layer.id ? updated : l))
      );
      if (onLayersChange) {
        onLayersChange(layers.map((l) => (l.id === layer.id ? updated : l)));
      }
    } catch (error) {
      toast.error('Error updating opacity: ' + error.message);
    }
  };

  const handleDeleteLayer = async (layer) => {
    if (!window.confirm(`Delete layer "${layer.name}"?`)) return;

    try {
      await layerService.deleteLayer(layer.id);
      setLayers((prev) => prev.filter((l) => l.id !== layer.id));
      if (onLayersChange) {
        onLayersChange(layers.filter((l) => l.id !== layer.id));
      }
      toast.success('Layer deleted');
    } catch (error) {
      toast.error('Error deleting layer: ' + error.message);
    }
  };

  const handlePublishToGeoServer = async (layer) => {
    try {
      await geoserverService.publishLayer(
        'gis_workspace',
        'postgis_store',
        layer.name,
        layer.title
      );
      toast.success(`Layer "${layer.name}" published to GeoServer`);
    } catch (error) {
      toast.error('Error publishing layer: ' + error.message);
    }
  };

  if (loading) {
    return <div className="layer-list-loading">Loading layers...</div>;
  }

  return (
    <div className="layer-list">
      <div className="layer-list-header">
        <h3>Layers</h3>
        <button onClick={loadLayers} className="btn-refresh">
          Refresh
        </button>
      </div>
      {layers.length === 0 ? (
        <div className="no-layers">No layers found</div>
      ) : (
        <div className="layer-items">
          {layers.map((layer) => (
            <div key={layer.id} className="layer-item">
              <div className="layer-header">
                <input
                  type="checkbox"
                  checked={layer.visible}
                  onChange={() => handleVisibilityToggle(layer)}
                />
                <span className="layer-name">{layer.title || layer.name}</span>
              </div>
              <div className="layer-controls">
                <label>
                  Opacity:
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={layer.opacity}
                    onChange={(e) => handleOpacityChange(layer, e.target.value)}
                  />
                  <span>{Math.round(layer.opacity * 100)}%</span>
                </label>
              </div>
              <div className="layer-actions">
                <button
                  onClick={() => handlePublishToGeoServer(layer)}
                  className="btn-publish"
                  title="Publish to GeoServer"
                >
                  Publish
                </button>
                <button
                  onClick={() => handleDeleteLayer(layer)}
                  className="btn-delete"
                  title="Delete layer"
                >
                  Delete
                </button>
              </div>
              {layer.description && (
                <div className="layer-description">{layer.description}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LayerList;
