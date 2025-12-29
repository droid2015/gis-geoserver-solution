import React, { useState } from 'react';
import queryService from '../../services/queryService';
import { toast } from 'react-toastify';
import './SpatialQuery.css';

const SpatialQuery = ({ onQueryResults }) => {
  const [layerName, setLayerName] = useState('vietnam_cities');
  const [queryType, setQueryType] = useState('bbox');
  const [bbox, setBBox] = useState({
    minx: 105.0,
    miny: 10.0,
    maxx: 109.0,
    maxy: 22.0,
  });
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    try {
      let results;
      if (queryType === 'bbox') {
        results = await queryService.queryBBox(layerName, [
          bbox.minx,
          bbox.miny,
          bbox.maxx,
          bbox.maxy,
        ]);
      }
      
      if (results && results.features) {
        toast.success(`Found ${results.count} features`);
        if (onQueryResults) {
          onQueryResults(results);
        }
      } else {
        toast.info('No features found');
      }
    } catch (error) {
      toast.error('Query error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="spatial-query">
      <h3>Spatial Query</h3>
      
      <div className="form-group">
        <label>Layer Name:</label>
        <input
          type="text"
          value={layerName}
          onChange={(e) => setLayerName(e.target.value)}
          placeholder="e.g., vietnam_cities"
        />
      </div>

      <div className="form-group">
        <label>Query Type:</label>
        <select value={queryType} onChange={(e) => setQueryType(e.target.value)}>
          <option value="bbox">Bounding Box</option>
          <option value="intersect">Intersect</option>
          <option value="buffer">Buffer</option>
          <option value="within">Within</option>
        </select>
      </div>

      {queryType === 'bbox' && (
        <div className="bbox-inputs">
          <div className="form-row">
            <div className="form-group">
              <label>Min X:</label>
              <input
                type="number"
                value={bbox.minx}
                onChange={(e) => setBBox({ ...bbox, minx: parseFloat(e.target.value) })}
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label>Min Y:</label>
              <input
                type="number"
                value={bbox.miny}
                onChange={(e) => setBBox({ ...bbox, miny: parseFloat(e.target.value) })}
                step="0.1"
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Max X:</label>
              <input
                type="number"
                value={bbox.maxx}
                onChange={(e) => setBBox({ ...bbox, maxx: parseFloat(e.target.value) })}
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label>Max Y:</label>
              <input
                type="number"
                value={bbox.maxy}
                onChange={(e) => setBBox({ ...bbox, maxy: parseFloat(e.target.value) })}
                step="0.1"
              />
            </div>
          </div>
        </div>
      )}

      <button onClick={handleQuery} disabled={loading} className="btn-query">
        {loading ? 'Querying...' : 'Execute Query'}
      </button>
    </div>
  );
};

export default SpatialQuery;
