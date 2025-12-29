#!/usr/bin/env python3
"""
GeoServer Auto-Configuration Script
Waits for GeoServer to be ready and configures workspace, datastore, and publishes sample layers
"""

import time
import requests
from requests.auth import HTTPBasicAuth
import os
import sys

# Configuration
GEOSERVER_URL = os.getenv('GEOSERVER_URL', 'http://geoserver:8080/geoserver')
GEOSERVER_USER = os.getenv('GEOSERVER_ADMIN_USER', 'admin')
GEOSERVER_PASSWORD = os.getenv('GEOSERVER_ADMIN_PASSWORD', 'geoserver')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres-postgis')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'gisdb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'gisuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'changeme_gispassword')

REST_URL = f"{GEOSERVER_URL}/rest"
AUTH = HTTPBasicAuth(GEOSERVER_USER, GEOSERVER_PASSWORD)


def wait_for_geoserver(max_attempts=30, delay=10):
    """Wait for GeoServer to be ready"""
    print(f"Waiting for GeoServer at {GEOSERVER_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                f"{REST_URL}/about/version.json",
                auth=AUTH,
                timeout=5
            )
            if response.status_code == 200:
                print("✅ GeoServer is ready!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_attempts}: GeoServer not ready yet...")
        
        time.sleep(delay)
    
    print("❌ GeoServer failed to start")
    return False


def create_workspace(workspace_name='gis_workspace'):
    """Create a workspace"""
    print(f"Creating workspace: {workspace_name}")
    
    # Check if workspace exists
    response = requests.get(
        f"{REST_URL}/workspaces/{workspace_name}.json",
        auth=AUTH
    )
    
    if response.status_code == 200:
        print(f"✅ Workspace '{workspace_name}' already exists")
        return True
    
    # Create workspace
    data = {
        "workspace": {
            "name": workspace_name
        }
    }
    
    response = requests.post(
        f"{REST_URL}/workspaces",
        auth=AUTH,
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Workspace '{workspace_name}' created successfully")
        return True
    else:
        print(f"❌ Failed to create workspace: {response.status_code} - {response.text}")
        return False


def create_postgis_datastore(workspace='gis_workspace', datastore='postgis_store'):
    """Create PostGIS datastore"""
    print(f"Creating PostGIS datastore: {datastore}")
    
    # Check if datastore exists
    response = requests.get(
        f"{REST_URL}/workspaces/{workspace}/datastores/{datastore}.json",
        auth=AUTH
    )
    
    if response.status_code == 200:
        print(f"✅ Datastore '{datastore}' already exists")
        return True
    
    # Create datastore
    data = {
        "dataStore": {
            "name": datastore,
            "type": "PostGIS",
            "enabled": True,
            "connectionParameters": {
                "entry": [
                    {"@key": "host", "$": POSTGRES_HOST},
                    {"@key": "port", "$": str(POSTGRES_PORT)},
                    {"@key": "database", "$": POSTGRES_DB},
                    {"@key": "user", "$": POSTGRES_USER},
                    {"@key": "passwd", "$": POSTGRES_PASSWORD},
                    {"@key": "dbtype", "$": "postgis"},
                    {"@key": "schema", "$": "public"},
                    {"@key": "Expose primary keys", "$": "true"},
                ]
            }
        }
    }
    
    response = requests.post(
        f"{REST_URL}/workspaces/{workspace}/datastores",
        auth=AUTH,
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Datastore '{datastore}' created successfully")
        return True
    else:
        print(f"❌ Failed to create datastore: {response.status_code} - {response.text}")
        return False


def publish_layer(workspace='gis_workspace', datastore='postgis_store', 
                  table_name='vietnam_cities', title='Vietnam Cities'):
    """Publish a PostGIS table as a layer"""
    print(f"Publishing layer: {table_name}")
    
    # Check if layer exists
    response = requests.get(
        f"{REST_URL}/workspaces/{workspace}/layers/{table_name}.json",
        auth=AUTH
    )
    
    if response.status_code == 200:
        print(f"✅ Layer '{table_name}' already exists")
        return True
    
    # Publish layer
    data = {
        "featureType": {
            "name": table_name,
            "nativeName": table_name,
            "title": title,
            "srs": "EPSG:4326",
            "enabled": True,
            "store": {
                "@class": "dataStore",
                "name": f"{workspace}:{datastore}"
            }
        }
    }
    
    response = requests.post(
        f"{REST_URL}/workspaces/{workspace}/datastores/{datastore}/featuretypes",
        auth=AUTH,
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Layer '{table_name}' published successfully")
        return True
    else:
        print(f"❌ Failed to publish layer: {response.status_code} - {response.text}")
        return False


def publish_highway_layer():
    """Publish highways layer to GeoServer"""
    print("Publishing highways layer...")
    
    workspace = 'gis_workspace'
    datastore = 'postgis_store'
    
    layer_config = {
        "featureType": {
            "name": "highways",
            "nativeName": "highways",
            "title": "Vietnam Highways",
            "abstract": "Major highways and expressways in Vietnam",
            "srs": "EPSG:4326",
            "enabled": True,
            "store": {
                "@class": "dataStore",
                "name": f"{workspace}:{datastore}"
            }
        }
    }
    
    response = requests.post(
        f"{REST_URL}/workspaces/{workspace}/datastores/{datastore}/featuretypes",
        auth=AUTH,
        headers={"Content-Type": "application/json"},
        json=layer_config
    )
    
    if response.status_code in [200, 201]:
        print("✅ Highways layer published")
        
        # Apply style
        style_data = {
            "layer": {
                "defaultStyle": {
                    "name": "highway_style"
                }
            }
        }
        
        requests.put(
            f"{REST_URL}/layers/{workspace}:highways",
            auth=AUTH,
            headers={"Content-Type": "application/json"},
            json=style_data
        )
        print("✅ Highway style applied")
    else:
        print(f"✗ Failed to publish highways layer: {response.text}")



def main():
    """Main configuration function"""
    print("=" * 60)
    print("GeoServer Auto-Configuration Script")
    print("=" * 60)
    
    # Wait for GeoServer
    if not wait_for_geoserver():
        sys.exit(1)
    
    # Create workspace
    if not create_workspace('gis_workspace'):
        sys.exit(1)
    
    # Create datastore
    if not create_postgis_datastore('gis_workspace', 'postgis_store'):
        sys.exit(1)
    
    # Publish sample layer
    if not publish_layer('gis_workspace', 'postgis_store', 'vietnam_cities', 'Vietnam Cities'):
        sys.exit(1)
    
    # Publish highways layer
    publish_highway_layer()
    
    print("=" * 60)
    print("✅ GeoServer configuration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
