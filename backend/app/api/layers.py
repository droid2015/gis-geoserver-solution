from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.spatial import Layer, Highway
from app.schemas.spatial import LayerResponse, LayerCreate, LayerUpdate, HighwayGeoJSON
from sqlalchemy import text, func
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/layers", tags=["layers"])


@router.get("", response_model=List[LayerResponse])
def list_layers(db: Session = Depends(get_db)):
    """List all layers"""
    try:
        layers = db.query(Layer).all()
        return layers
    except Exception as e:
        logger.error(f"Error listing layers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{layer_id}", response_model=LayerResponse)
def get_layer(layer_id: int, db: Session = Depends(get_db)):
    """Get layer by ID"""
    try:
        layer = db.query(Layer).filter(Layer.id == layer_id).first()
        if not layer:
            raise HTTPException(status_code=404, detail="Layer not found")
        return layer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=LayerResponse)
def create_layer(layer: LayerCreate, db: Session = Depends(get_db)):
    """Create a new layer"""
    try:
        # Check if layer already exists
        existing = db.query(Layer).filter(Layer.name == layer.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Layer with this name already exists")
        
        db_layer = Layer(**layer.model_dump())
        db.add(db_layer)
        db.commit()
        db.refresh(db_layer)
        return db_layer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating layer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{layer_id}", response_model=LayerResponse)
def update_layer(layer_id: int, layer_update: LayerUpdate, db: Session = Depends(get_db)):
    """Update layer metadata"""
    try:
        db_layer = db.query(Layer).filter(Layer.id == layer_id).first()
        if not db_layer:
            raise HTTPException(status_code=404, detail="Layer not found")
        
        # Update only provided fields
        update_data = layer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_layer, field, value)
        
        db.commit()
        db.refresh(db_layer)
        return db_layer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating layer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{layer_id}")
def delete_layer(layer_id: int, db: Session = Depends(get_db)):
    """Delete a layer"""
    try:
        db_layer = db.query(Layer).filter(Layer.id == layer_id).first()
        if not db_layer:
            raise HTTPException(status_code=404, detail="Layer not found")
        
        layer_name = db_layer.name
        db.delete(db_layer)
        db.commit()
        
        # Optionally drop the table
        try:
            db.execute(text(f"DROP TABLE IF EXISTS {layer_name} CASCADE"))
            db.commit()
        except:
            pass  # Table might not exist
        
        return {"message": f"Layer {layer_name} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting layer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/highways", response_model=List[HighwayGeoJSON])
async def get_highways(db: Session = Depends(get_db)):
    """Get all highways as GeoJSON"""
    try:
        highways = db.query(Highway).all()
        
        result = []
        for highway in highways:
            # Get the geometry as GeoJSON
            geom_json = db.scalar(func.ST_AsGeoJSON(highway.geom))
            
            highway_dict = {
                "id": highway.id,
                "name": highway.name,
                "name_en": highway.name_en,
                "type": highway.type,
                "length_km": highway.length_km,
                "lanes": highway.lanes,
                "max_speed": highway.max_speed,
                "status": highway.status,
                "start_point": highway.start_point,
                "end_point": highway.end_point,
                "opened_date": highway.opened_date,
                "description": highway.description,
                "created_at": highway.created_at,
                "geometry": json.loads(geom_json) if geom_json else None
            }
            result.append(highway_dict)
        
        return result
    except Exception as e:
        logger.error(f"Error getting highways: {e}")
        raise HTTPException(status_code=500, detail=str(e))
