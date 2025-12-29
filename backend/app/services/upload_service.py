import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import fiona
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2 import WKTElement
import logging

logger = logging.getLogger(__name__)


class UploadService:
    """Service for file upload and processing"""
    
    @staticmethod
    async def process_shapefile(
        db: Session,
        file_path: str,
        layer_name: str
    ) -> Dict[str, Any]:
        """Process and import shapefile to PostGIS"""
        temp_dir = None
        try:
            # Create temporary directory for extraction
            temp_dir = tempfile.mkdtemp()
            
            # Extract zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find .shp file
            shp_file = None
            for file in os.listdir(temp_dir):
                if file.endswith('.shp'):
                    shp_file = os.path.join(temp_dir, file)
                    break
            
            if not shp_file:
                return {
                    "success": False,
                    "message": "No .shp file found in the zip archive",
                    "errors": ["Missing .shp file"]
                }
            
            # Read shapefile with fiona
            with fiona.open(shp_file, 'r') as src:
                # Get schema information
                geom_type = src.schema['geometry']
                crs = src.crs.get('init', 'epsg:4326') if src.crs else 'epsg:4326'
                srid = int(crs.split(':')[1]) if ':' in crs else 4326
                
                # Create table dynamically
                # Get first feature to infer schema
                features = list(src)
                if not features:
                    return {
                        "success": False,
                        "message": "Shapefile contains no features",
                        "errors": ["Empty shapefile"]
                    }
                
                first_feature = features[0]
                properties = first_feature['properties']
                
                # Build CREATE TABLE statement
                columns = []
                columns.append("id SERIAL PRIMARY KEY")
                
                for prop_name, prop_value in properties.items():
                    # Sanitize column name
                    col_name = prop_name.lower().replace(' ', '_').replace('-', '_')
                    
                    # Infer data type
                    if isinstance(prop_value, int):
                        col_type = "INTEGER"
                    elif isinstance(prop_value, float):
                        col_type = "DOUBLE PRECISION"
                    else:
                        col_type = "TEXT"
                    
                    columns.append(f"{col_name} {col_type}")
                
                # Add geometry column
                columns.append(f"geom GEOMETRY({geom_type.upper()}, {srid})")
                
                # Create table
                create_table = f"CREATE TABLE IF NOT EXISTS {layer_name} ({', '.join(columns)})"
                db.execute(text(create_table))
                db.commit()
                
                # Insert features
                feature_count = 0
                for feature in features:
                    props = feature['properties']
                    geom = feature['geometry']
                    
                    # Build INSERT statement
                    prop_names = [name.lower().replace(' ', '_').replace('-', '_') for name in props.keys()]
                    prop_values = list(props.values())
                    
                    geom_wkt = f"SRID={srid};{json.dumps(geom)}"
                    
                    columns_str = ', '.join(prop_names + ['geom'])
                    placeholders = ', '.join([f':p{i}' for i in range(len(prop_values))] + ['ST_GeomFromGeoJSON(:geom)'])
                    
                    insert_query = f"INSERT INTO {layer_name} ({columns_str}) VALUES ({placeholders})"
                    
                    params = {f'p{i}': val for i, val in enumerate(prop_values)}
                    params['geom'] = json.dumps(geom)
                    
                    db.execute(text(insert_query), params)
                    feature_count += 1
                
                db.commit()
                
                # Create spatial index
                db.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{layer_name}_geom ON {layer_name} USING GIST(geom)"))
                db.commit()
                
                return {
                    "success": True,
                    "message": f"Successfully imported {feature_count} features",
                    "layer_name": layer_name,
                    "feature_count": feature_count
                }
                
        except Exception as e:
            logger.error(f"Error processing shapefile: {e}")
            return {
                "success": False,
                "message": f"Error processing shapefile: {str(e)}",
                "errors": [str(e)]
            }
        finally:
            # Clean up temporary directory
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    @staticmethod
    async def process_geojson(
        db: Session,
        file_path: str,
        layer_name: str
    ) -> Dict[str, Any]:
        """Process and import GeoJSON to PostGIS"""
        try:
            # Read GeoJSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            if geojson_data.get('type') != 'FeatureCollection':
                return {
                    "success": False,
                    "message": "Invalid GeoJSON: must be a FeatureCollection",
                    "errors": ["Not a FeatureCollection"]
                }
            
            features = geojson_data.get('features', [])
            if not features:
                return {
                    "success": False,
                    "message": "GeoJSON contains no features",
                    "errors": ["Empty FeatureCollection"]
                }
            
            # Get first feature to infer schema
            first_feature = features[0]
            properties = first_feature.get('properties', {})
            geom = first_feature.get('geometry', {})
            geom_type = geom.get('type', 'Point').upper()
            
            # Build CREATE TABLE statement
            columns = []
            columns.append("id SERIAL PRIMARY KEY")
            
            for prop_name, prop_value in properties.items():
                # Sanitize column name
                col_name = prop_name.lower().replace(' ', '_').replace('-', '_')
                
                # Infer data type
                if isinstance(prop_value, int):
                    col_type = "INTEGER"
                elif isinstance(prop_value, float):
                    col_type = "DOUBLE PRECISION"
                elif isinstance(prop_value, bool):
                    col_type = "BOOLEAN"
                else:
                    col_type = "TEXT"
                
                columns.append(f"{col_name} {col_type}")
            
            # Add geometry column
            columns.append(f"geom GEOMETRY({geom_type}, 4326)")
            
            # Create table
            create_table = f"CREATE TABLE IF NOT EXISTS {layer_name} ({', '.join(columns)})"
            db.execute(text(create_table))
            db.commit()
            
            # Insert features
            feature_count = 0
            for feature in features:
                props = feature.get('properties', {})
                geom = feature.get('geometry', {})
                
                if not geom:
                    continue
                
                # Build INSERT statement
                prop_names = [name.lower().replace(' ', '_').replace('-', '_') for name in props.keys()]
                prop_values = list(props.values())
                
                columns_str = ', '.join(prop_names + ['geom'])
                placeholders = ', '.join([f':p{i}' for i in range(len(prop_values))] + ['ST_GeomFromGeoJSON(:geom)'])
                
                insert_query = f"INSERT INTO {layer_name} ({columns_str}) VALUES ({placeholders})"
                
                params = {f'p{i}': val for i, val in enumerate(prop_values)}
                params['geom'] = json.dumps(geom)
                
                db.execute(text(insert_query), params)
                feature_count += 1
            
            db.commit()
            
            # Create spatial index
            db.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{layer_name}_geom ON {layer_name} USING GIST(geom)"))
            db.commit()
            
            return {
                "success": True,
                "message": f"Successfully imported {feature_count} features",
                "layer_name": layer_name,
                "feature_count": feature_count
            }
            
        except Exception as e:
            logger.error(f"Error processing GeoJSON: {e}")
            return {
                "success": False,
                "message": f"Error processing GeoJSON: {str(e)}",
                "errors": [str(e)]
            }


upload_service = UploadService()
