from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings
from app.database import get_db, engine
from app.api import layers, geoserver, upload, query
from app.services.geoserver_service import geoserver_service
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GIS GeoServer Solution API",
    description="REST API for GIS operations with GeoServer and PostGIS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting GIS GeoServer Solution API")
    logger.info(f"Database URL: {settings.database_url.split('@')[1]}")  # Log without password
    logger.info(f"GeoServer URL: {settings.GEOSERVER_URL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down GIS GeoServer Solution API")


# Health check endpoints
@app.get("/api/health", tags=["health"])
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "service": "GIS GeoServer Solution API",
        "version": "1.0.0"
    }


@app.get("/api/health/database", tags=["health"])
async def database_health_check():
    """Check PostgreSQL/PostGIS connection"""
    try:
        db = next(get_db())
        # Test query
        result = db.execute(text("SELECT PostGIS_version()"))
        version = result.scalar()
        return {
            "status": "healthy",
            "database": "PostgreSQL + PostGIS",
            "postgis_version": version
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "PostgreSQL + PostGIS",
            "error": str(e)
        }


@app.get("/api/health/geoserver", tags=["health"])
async def geoserver_health_check():
    """Check GeoServer connection"""
    try:
        is_connected = await geoserver_service.check_connection()
        if is_connected:
            return {
                "status": "healthy",
                "service": "GeoServer",
                "url": settings.GEOSERVER_URL
            }
        else:
            return {
                "status": "unhealthy",
                "service": "GeoServer",
                "url": settings.GEOSERVER_URL,
                "error": "Cannot connect to GeoServer"
            }
    except Exception as e:
        logger.error(f"GeoServer health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "GeoServer",
            "error": str(e)
        }


# Include routers
app.include_router(layers.router)
app.include_router(geoserver.router)
app.include_router(upload.router)
app.include_router(query.router)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "GIS GeoServer Solution API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
