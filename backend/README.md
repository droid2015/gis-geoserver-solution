# FastAPI GIS Backend

Backend REST API cho hệ thống GIS sử dụng FastAPI, PostgreSQL+PostGIS và GeoServer.

## Tính năng

- Health check endpoints
- Layer management (CRUD)
- GeoServer integration
- File upload (Shapefile, GeoJSON)
- Spatial queries (bbox, intersect, buffer, within)

## Cấu trúc

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API endpoints
│   └── services/            # Business logic services
├── tests/                   # Tests
├── requirements.txt         # Dependencies
├── Dockerfile              # Docker image
└── README.md
```

## API Endpoints

Xem full documentation tại: http://localhost:8000/docs

### Health Checks
- `GET /api/health` - API status
- `GET /api/health/database` - Database connection
- `GET /api/health/geoserver` - GeoServer connection

### Layers
- `GET /api/layers` - List all layers
- `GET /api/layers/{id}` - Get layer by ID
- `POST /api/layers` - Create layer
- `PUT /api/layers/{id}` - Update layer
- `DELETE /api/layers/{id}` - Delete layer

### GeoServer
- `GET /api/geoserver/workspaces` - List workspaces
- `POST /api/geoserver/workspaces` - Create workspace
- `GET /api/geoserver/layers` - List layers
- `POST /api/geoserver/publish` - Publish layer
- `DELETE /api/geoserver/layers/{workspace}/{name}` - Delete layer
- `GET /api/geoserver/styles` - List styles

### Upload
- `POST /api/upload/shapefile` - Upload shapefile
- `POST /api/upload/geojson` - Upload GeoJSON

### Query
- `POST /api/query/bbox` - Bounding box query
- `POST /api/query/intersect` - Intersection query
- `POST /api/query/buffer` - Buffer query
- `POST /api/query/within` - Within query
- `GET /api/query/attributes/{layer}` - Get layer attributes

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest
```
