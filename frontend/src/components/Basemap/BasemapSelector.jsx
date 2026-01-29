import React, { useState } from 'react';
import './BasemapSelector.css';

const BasemapSelector = ({ onBasemapChange }) => {
  const [selectedBasemap, setSelectedBasemap] = useState('osm');

  const basemaps = [
    { id: 'osm', name: 'OpenStreetMap', description: 'Open source map' },
    { id: 'oracle', name: 'Oracle Tiles', description: 'Custom basemap from Oracle' }
  ];

  const handleChange = (basemapId) => {
    setSelectedBasemap(basemapId);
    if (onBasemapChange) {
      onBasemapChange(basemapId);
    }
  };

  return (
    <div className="basemap-selector">
      <h3>Basemap</h3>
      <div className="basemap-options">
        {basemaps.map((basemap) => (
          <div key={basemap.id} className="basemap-option">
            <label>
              <input
                type="radio"
                name="basemap"
                value={basemap.id}
                checked={selectedBasemap === basemap.id}
                onChange={() => handleChange(basemap.id)}
              />
              <div className="basemap-info">
                <span className="basemap-name">{basemap.name}</span>
                <span className="basemap-description">{basemap.description}</span>
              </div>
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BasemapSelector;
