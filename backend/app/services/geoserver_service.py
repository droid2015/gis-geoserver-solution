import httpx
from typing import Optional, Dict, Any, List
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GeoServerService:
    """Service for interacting with GeoServer REST API"""
    
    def __init__(self):
        self.base_url = settings.GEOSERVER_URL
        self.auth = (settings.GEOSERVER_ADMIN_USER, settings.GEOSERVER_ADMIN_PASSWORD)
        self.rest_url = f"{self.base_url}/rest"
    
    async def check_connection(self) -> bool:
        """Check if GeoServer is accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.rest_url}/about/version.json",
                    auth=self.auth,
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"GeoServer connection error: {e}")
            return False
    
    async def list_workspaces(self) -> List[Dict[str, Any]]:
        """List all workspaces"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.rest_url}/workspaces.json",
                    auth=self.auth
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("workspaces", {}).get("workspace", [])
                return []
        except Exception as e:
            logger.error(f"Error listing workspaces: {e}")
            return []
    
    async def create_workspace(self, name: str) -> bool:
        """Create a new workspace"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.rest_url}/workspaces",
                    auth=self.auth,
                    json={"workspace": {"name": name}},
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Error creating workspace: {e}")
            return False
    
    async def create_datastore(
        self, 
        workspace: str, 
        name: str,
        db_host: str,
        db_port: int,
        db_name: str,
        db_user: str,
        db_password: str
    ) -> bool:
        """Create a PostGIS datastore"""
        try:
            datastore_data = {
                "dataStore": {
                    "name": name,
                    "type": "PostGIS",
                    "enabled": True,
                    "connectionParameters": {
                        "entry": [
                            {"@key": "host", "$": db_host},
                            {"@key": "port", "$": str(db_port)},
                            {"@key": "database", "$": db_name},
                            {"@key": "user", "$": db_user},
                            {"@key": "passwd", "$": db_password},
                            {"@key": "dbtype", "$": "postgis"},
                            {"@key": "schema", "$": "public"},
                        ]
                    }
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.rest_url}/workspaces/{workspace}/datastores",
                    auth=self.auth,
                    json=datastore_data,
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Error creating datastore: {e}")
            return False
    
    async def publish_layer(
        self,
        workspace: str,
        datastore: str,
        table_name: str,
        title: Optional[str] = None
    ) -> bool:
        """Publish a PostGIS table as a layer"""
        try:
            feature_type_data = {
                "featureType": {
                    "name": table_name,
                    "nativeName": table_name,
                    "title": title or table_name,
                    "srs": "EPSG:4326",
                    "enabled": True
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.rest_url}/workspaces/{workspace}/datastores/{datastore}/featuretypes",
                    auth=self.auth,
                    json=feature_type_data,
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Error publishing layer: {e}")
            return False
    
    async def list_layers(self, workspace: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all layers or layers in a workspace"""
        try:
            url = f"{self.rest_url}/layers.json"
            if workspace:
                url = f"{self.rest_url}/workspaces/{workspace}/layers.json"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, auth=self.auth)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("layers", {}).get("layer", [])
                return []
        except Exception as e:
            logger.error(f"Error listing layers: {e}")
            return []
    
    async def delete_layer(self, workspace: str, layer_name: str, recursive: bool = True) -> bool:
        """Delete a layer"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.rest_url}/workspaces/{workspace}/layers/{layer_name}",
                    auth=self.auth,
                    params={"recurse": str(recursive).lower()}
                )
                return response.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Error deleting layer: {e}")
            return False
    
    async def get_layer_info(self, workspace: str, layer_name: str) -> Optional[Dict[str, Any]]:
        """Get layer information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.rest_url}/workspaces/{workspace}/layers/{layer_name}.json",
                    auth=self.auth
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error getting layer info: {e}")
            return None
    
    async def list_styles(self) -> List[Dict[str, Any]]:
        """List all styles"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.rest_url}/styles.json",
                    auth=self.auth
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("styles", {}).get("style", [])
                return []
        except Exception as e:
            logger.error(f"Error listing styles: {e}")
            return []


geoserver_service = GeoServerService()
