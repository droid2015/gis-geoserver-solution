from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.spatial_service import spatial_service
from app.schemas.spatial import BBoxQuery, BufferQuery, IntersectQuery, WithinQuery
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/query", tags=["query"])


@router.post("/bbox")
def query_bbox(query: BBoxQuery, db: Session = Depends(get_db)):
    """Query features by bounding box"""
    try:
        features = spatial_service.query_bbox(
            db=db,
            layer_name=query.layer_name,
            minx=query.minx,
            miny=query.miny,
            maxx=query.maxx,
            maxy=query.maxy,
            srid=query.srid
        )
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "count": len(features)
        }
    except Exception as e:
        logger.error(f"Error in bbox query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/intersect")
def query_intersect(query: IntersectQuery, db: Session = Depends(get_db)):
    """Query features that intersect with a geometry"""
    try:
        features = spatial_service.query_intersect(
            db=db,
            layer_name=query.layer_name,
            geometry=query.geometry,
            srid=query.srid
        )
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "count": len(features)
        }
    except Exception as e:
        logger.error(f"Error in intersect query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/buffer")
def query_buffer(query: BufferQuery, db: Session = Depends(get_db)):
    """Query features within a buffer distance"""
    try:
        features = spatial_service.query_buffer(
            db=db,
            layer_name=query.layer_name,
            geometry=query.geometry,
            distance=query.distance,
            srid=query.srid
        )
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "count": len(features)
        }
    except Exception as e:
        logger.error(f"Error in buffer query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/within")
def query_within(query: WithinQuery, db: Session = Depends(get_db)):
    """Query features within a polygon"""
    try:
        features = spatial_service.query_within(
            db=db,
            layer_name=query.layer_name,
            geometry=query.geometry,
            srid=query.srid
        )
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "count": len(features)
        }
    except Exception as e:
        logger.error(f"Error in within query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attributes/{layer_name}")
def get_attributes(layer_name: str, db: Session = Depends(get_db)):
    """Get layer attribute information"""
    try:
        attributes = spatial_service.get_layer_attributes(db, layer_name)
        if not attributes:
            raise HTTPException(status_code=404, detail="Layer not found")
        return attributes
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting attributes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
