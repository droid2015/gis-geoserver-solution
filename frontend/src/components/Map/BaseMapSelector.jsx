import React from 'react';
import './BaseMapSelector.css';

const BaseMapSelector = ({ selectedBasemap, onBasemapChange }) => {
  return (
    <div className="basemap-selector">
      <h4>Base Map</h4>
      <div className="basemap-options">
        <label className="basemap-option">
          <input
            type="radio"
            name="basemap"
            value="osm"
            checked={selectedBasemap === 'osm'}
            onChange={(e) => onBasemapChange(e.target.value)}
          />
          <span>OpenStreetMap</span>
        </label>
        <label className="basemap-option">
          <input
            type="radio"
            name="basemap"
            value="oracle"
            checked={selectedBasemap === 'oracle'}
            onChange={(e) => onBasemapChange(e.target.value)}
          />
          <span>Oracle Tiles</span>
        </label>
      </div>
    </div>
  );
};

export default BaseMapSelector;
