import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="app-header">
      <h1>GIS GeoServer Solution</h1>
      <div className="header-actions">
        <a href="/docs" target="_blank" rel="noopener noreferrer">
          API Docs
        </a>
        <a href={process.env.REACT_APP_GEOSERVER_URL} target="_blank" rel="noopener noreferrer">
          GeoServer
        </a>
      </div>
    </header>
  );
};

export default Header;
