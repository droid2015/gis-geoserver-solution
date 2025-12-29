# API Documentation

REST API documentation cho GIS GeoServer Solution.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

FastAPI cung cấp interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Hiện tại API không yêu cầu authentication. Trong production, nên implement authentication.

## Health Check Endpoints

### GET /api/health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "GIS GeoServer Solution API",
  "version": "1.0.0"
}
```

### GET /api/health/database

Check PostgreSQL/PostGIS connection.

**Response:**
```json
{
  "status": "healthy",
  "database": "PostgreSQL + PostGIS",
  "postgis_version": "3.4 USE_GEOS=1 USE_PROJ=1..."
}
```

### GET /api/health/geoserver

Check GeoServer connection.

**Response:**
```json
{
  "status": "healthy",
  "service": "GeoServer",
  "url": "http://geoserver:8080/geoserver"
}
```

## Layer Management

### GET /api/layers

List all layers.

**Response:**
```json
[
  {
    "id": 1,
    "name": "vietnam_cities",
    "title": "Các thành phố Việt Nam",
    "description": "Sample data - Vietnam cities",
    "geometry_type": "Point",
    "srid": 4326,
    "visible": true,
    "opacity": 1.0,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": null
  }
]
```

### GET /api/layers/{layer_id}

Get layer by ID.

### POST /api/layers

Create new layer.

**Request Body:**
```json
{
  "name": "my_layer",
  "title": "My Layer",
  "description": "Layer description",
  "geometry_type": "Point",
  "srid": 4326,
  "visible": true,
  "opacity": 1.0
}
```

### PUT /api/layers/{layer_id}

Update layer metadata.

### DELETE /api/layers/{layer_id}

Delete layer.

## Upload Endpoints

### POST /api/upload/shapefile

Upload shapefile (as zip).

**Form Data:**
- `file`: ZIP file containing .shp, .shx, .dbf, .prj
- `layer_name`: Name for the layer

**Response:**
```json
{
  "success": true,
  "message": "Successfully imported 10 features",
  "layer_name": "my_layer",
  "feature_count": 10
}
```

### POST /api/upload/geojson

Upload GeoJSON file.

**Form Data:**
- `file`: GeoJSON file
- `layer_name`: Name for the layer

## Spatial Query Endpoints

### POST /api/query/bbox

Bounding box query.

**Request Body:**
```json
{
  "layer_name": "vietnam_cities",
  "minx": 105.0,
  "miny": 10.0,
  "maxx": 109.0,
  "maxy": 22.0,
  "srid": 4326
}
```

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [...],
  "count": 10
}
```

### POST /api/query/intersect

Intersection query.

**Request Body:**
```json
{
  "layer_name": "vietnam_cities",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[105, 10], [109, 10], [109, 22], [105, 22], [105, 10]]]
  },
  "srid": 4326
}
```

### POST /api/query/buffer

Buffer query.

**Request Body:**
```json
{
  "layer_name": "vietnam_cities",
  "geometry": {
    "type": "Point",
    "coordinates": [106.6297, 10.8231]
  },
  "distance": 1.0,
  "srid": 4326
}
```

### POST /api/query/within

Within query (point in polygon).

**Request Body:**
```json
{
  "layer_name": "vietnam_cities",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[105, 10], [109, 10], [109, 22], [105, 22], [105, 10]]]
  },
  "srid": 4326
}
```

### GET /api/query/attributes/{layer_name}

Get layer attributes info.

**Response:**
```json
{
  "layer_name": "vietnam_cities",
  "columns": [
    {"name": "id", "type": "integer"},
    {"name": "name", "type": "character varying"},
    {"name": "population", "type": "integer"}
  ],
  "feature_count": 10
}
```

## GeoServer Integration

### GET /api/geoserver/workspaces

List all workspaces.

### POST /api/geoserver/workspaces?workspace_name={name}

Create workspace.

### GET /api/geoserver/layers

List all published layers.

### POST /api/geoserver/publish

Publish PostGIS table to GeoServer.

**Query Parameters:**
- `workspace`: Workspace name
- `datastore`: Datastore name
- `table_name`: PostGIS table name
- `title`: Layer title (optional)

### DELETE /api/geoserver/layers/{workspace}/{layer_name}

Delete published layer.

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message here"
}
```

**Common HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Examples

### Upload and Query Workflow

```bash
# 1. Upload GeoJSON
curl -X POST http://localhost:8000/api/upload/geojson \
  -F "file=@cities.geojson" \
  -F "layer_name=my_cities"

# 2. Query features
curl -X POST http://localhost:8000/api/query/bbox \
  -H "Content-Type: application/json" \
  -d '{
    "layer_name": "my_cities",
    "minx": 105,
    "miny": 10,
    "maxx": 109,
    "maxy": 22,
    "srid": 4326
  }'

# 3. Publish to GeoServer
curl -X POST "http://localhost:8000/api/geoserver/publish?workspace=gis_workspace&datastore=postgis_store&table_name=my_cities&title=My Cities"

# 4. Get layer info
curl http://localhost:8000/api/layers
```

For more examples, visit: http://localhost:8000/docs
