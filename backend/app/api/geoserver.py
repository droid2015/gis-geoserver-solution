from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.geoserver_service import geoserver_service
from app.config import settings
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/geoserver", tags=["geoserver"])


@router.get("/workspaces")
async def list_workspaces():
    """List all GeoServer workspaces"""
    try:
        workspaces = await geoserver_service.list_workspaces()
        return {"workspaces": workspaces}
    except Exception as e:
        logger.error(f"Error listing workspaces: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workspaces")
async def create_workspace(workspace_name: str):
    """Create a new GeoServer workspace"""
    try:
        success = await geoserver_service.create_workspace(workspace_name)
        if success:
            return {"message": f"Workspace '{workspace_name}' created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create workspace")
    except Exception as e:
        logger.error(f"Error creating workspace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/layers")
async def list_layers(workspace: str = None):
    """List all GeoServer layers"""
    try:
        layers = await geoserver_service.list_layers(workspace)
        return {"layers": layers}
    except Exception as e:
        logger.error(f"Error listing layers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/publish")
async def publish_layer(
    workspace: str,
    datastore: str,
    table_name: str,
    title: str = None,
    db: Session = Depends(get_db)
):
    """Publish a PostGIS table as a GeoServer layer"""
    try:
        # First, ensure workspace exists
        workspaces = await geoserver_service.list_workspaces()
        workspace_names = [w.get('name') for w in workspaces]
        
        if workspace not in workspace_names:
            # Create workspace
            await geoserver_service.create_workspace(workspace)
        
        # Check if datastore exists, if not create it
        datastores_exist = False
        try:
            # Try to create datastore (will fail if exists, which is ok)
            await geoserver_service.create_datastore(
                workspace=workspace,
                name=datastore,
                db_host=settings.POSTGRES_HOST,
                db_port=settings.POSTGRES_PORT,
                db_name=settings.POSTGRES_DB,
                db_user=settings.POSTGRES_USER,
                db_password=settings.POSTGRES_PASSWORD
            )
        except:
            pass  # Datastore might already exist
        
        # Publish layer
        success = await geoserver_service.publish_layer(
            workspace=workspace,
            datastore=datastore,
            table_name=table_name,
            title=title
        )
        
        if success:
            return {
                "message": f"Layer '{table_name}' published successfully",
                "workspace": workspace,
                "layer_name": table_name
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to publish layer")
    except Exception as e:
        logger.error(f"Error publishing layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/layers/{workspace}/{layer_name}")
async def delete_layer(workspace: str, layer_name: str):
    """Unpublish a GeoServer layer"""
    try:
        success = await geoserver_service.delete_layer(workspace, layer_name)
        if success:
            return {"message": f"Layer '{layer_name}' deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete layer")
    except Exception as e:
        logger.error(f"Error deleting layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/styles")
async def list_styles():
    """List all GeoServer styles"""
    try:
        styles = await geoserver_service.list_styles()
        return {"styles": styles}
    except Exception as e:
        logger.error(f"Error listing styles: {e}")
        raise HTTPException(status_code=500, detail=str(e))
