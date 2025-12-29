from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.upload_service import upload_service
from app.schemas.spatial import UploadResponse
from app.models.spatial import Layer
import os
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/shapefile", response_model=UploadResponse)
async def upload_shapefile(
    file: UploadFile = File(...),
    layer_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and import a shapefile (as zip)"""
    try:
        # Validate file extension
        if not file.filename.endswith('.zip'):
            raise HTTPException(status_code=400, detail="File must be a ZIP archive")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.zip")
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process shapefile
        result = await upload_service.process_shapefile(db, file_path, layer_name)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        # If successful, add layer metadata
        if result.get("success"):
            # Check if layer metadata exists
            existing_layer = db.query(Layer).filter(Layer.name == layer_name).first()
            if not existing_layer:
                new_layer = Layer(
                    name=layer_name,
                    title=layer_name,
                    description=f"Imported from shapefile: {file.filename}",
                    visible=True,
                    opacity=1.0
                )
                db.add(new_layer)
                db.commit()
        
        return UploadResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading shapefile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/geojson", response_model=UploadResponse)
async def upload_geojson(
    file: UploadFile = File(...),
    layer_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and import a GeoJSON file"""
    try:
        # Validate file extension
        if not (file.filename.endswith('.geojson') or file.filename.endswith('.json')):
            raise HTTPException(status_code=400, detail="File must be a GeoJSON file (.geojson or .json)")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.geojson")
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process GeoJSON
        result = await upload_service.process_geojson(db, file_path, layer_name)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        # If successful, add layer metadata
        if result.get("success"):
            # Check if layer metadata exists
            existing_layer = db.query(Layer).filter(Layer.name == layer_name).first()
            if not existing_layer:
                new_layer = Layer(
                    name=layer_name,
                    title=layer_name,
                    description=f"Imported from GeoJSON: {file.filename}",
                    visible=True,
                    opacity=1.0
                )
                db.add(new_layer)
                db.commit()
        
        return UploadResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading GeoJSON: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{task_id}")
def get_upload_status(task_id: str):
    """Get upload status (placeholder for async processing)"""
    # This would be implemented with Celery or similar for async processing
    return {
        "task_id": task_id,
        "status": "completed",
        "message": "Upload processing completed"
    }
