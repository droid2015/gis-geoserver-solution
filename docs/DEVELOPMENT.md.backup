# Development Guide

Guide cho developers muốn contribute hoặc customize GIS GeoServer Solution.

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development (without Docker)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=gisdb
export POSTGRES_USER=gisuser
export POSTGRES_PASSWORD=password
export GEOSERVER_URL=http://localhost:8080/geoserver
export GEOSERVER_ADMIN_USER=admin
export GEOSERVER_ADMIN_PASSWORD=geoserver

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export REACT_APP_API_URL=http://localhost:8000
export REACT_APP_GEOSERVER_URL=http://localhost:8080/geoserver

# Run development server
npm start
```

### Docker Development

```bash
# Start services
docker-compose up -d

# Watch logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose build backend
docker-compose up -d
```

## Project Structure

```
gis-geoserver-solution/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database setup
│   │   └── main.py        # FastAPI app
│   ├── tests/             # Tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API clients
│   │   └── utils/         # Utilities
│   └── package.json
└── docker-compose.yml
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Docstrings for functions/classes
- Keep functions small và focused

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def get_layers(db: Session, skip: int = 0, limit: int = 100) -> List[Layer]:
    """
    Get all layers from database
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum records to return
        
    Returns:
        List of Layer objects
    """
    return db.query(Layer).offset(skip).limit(limit).all()
```

### JavaScript/React (Frontend)
- Use ES6+ syntax
- Functional components with hooks
- PropTypes hoặc TypeScript
- CSS modules hoặc styled-components

```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const LayerList = ({ onLayersChange }) => {
  const [layers, setLayers] = useState([]);
  
  useEffect(() => {
    loadLayers();
  }, []);
  
  const loadLayers = async () => {
    // Implementation
  };
  
  return (
    <div className="layer-list">
      {/* JSX */}
    </div>
  );
};

LayerList.propTypes = {
  onLayersChange: PropTypes.func,
};

export default LayerList;
```

## Adding New Features

### Add New API Endpoint

1. Create schema trong `backend/app/schemas/`
2. Create service function trong `backend/app/services/`
3. Create API route trong `backend/app/api/`
4. Add router to `backend/app/main.py`

Example:

```python
# schemas/spatial.py
class NewQuery(BaseModel):
    layer_name: str
    param: str

# services/spatial_service.py
def new_query(db: Session, layer_name: str, param: str):
    # Implementation
    pass

# api/query.py
@router.post("/new-query")
def execute_new_query(query: NewQuery, db: Session = Depends(get_db)):
    results = spatial_service.new_query(db, query.layer_name, query.param)
    return results
```

### Add New Frontend Component

1. Create component trong `frontend/src/components/`
2. Create styles (CSS file)
3. Import và use trong parent component

```javascript
// components/NewFeature/NewFeature.jsx
import React from 'react';
import './NewFeature.css';

const NewFeature = () => {
  return (
    <div className="new-feature">
      {/* Content */}
    </div>
  );
};

export default NewFeature;

// components/NewFeature/NewFeature.css
.new-feature {
  padding: 15px;
  background: #fff;
}
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_api.py::test_health_check
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Database Migrations

Khi thay đổi models:

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Apply migration
docker-compose exec backend alembic upgrade head
```

## API Documentation

FastAPI tự động generate docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

### Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes
4. Test changes
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Create Pull Request

### Commit Messages

Follow conventional commits:
- `feat: Add new feature`
- `fix: Fix bug`
- `docs: Update documentation`
- `style: Format code`
- `refactor: Refactor code`
- `test: Add tests`
- `chore: Update dependencies`

## Debugging

### Backend Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugpy for VSCode
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

### Frontend Debugging

```javascript
// Use browser DevTools
console.log('Debug info:', data);
debugger; // Breakpoint
```

## Performance Optimization

### Backend
- Use database indexes
- Implement caching (Redis)
- Optimize spatial queries
- Use async operations

### Frontend
- Code splitting
- Lazy loading components
- Memoization (React.memo, useMemo)
- Optimize OpenLayers rendering

## Deployment

### Production Checklist

- [ ] Change all default passwords
- [ ] Set DEBUG=False
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Add authentication
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Use environment-specific configs

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenLayers Documentation](https://openlayers.org/)
- [PostGIS Documentation](https://postgis.net/docs/)
- [GeoServer Documentation](https://docs.geoserver.org/)
