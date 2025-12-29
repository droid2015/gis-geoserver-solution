from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
from geoalchemy2.shape import to_shape
from shapely.geometry import shape, mapping
import json
import logging

logger = logging.getLogger(__name__)


class SpatialService:
    """Service for spatial data operations"""
    
    @staticmethod
    def query_bbox(
        db: Session,
        layer_name: str,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        srid: int = 4326
    ) -> List[Dict[str, Any]]:
        """Query features within a bounding box"""
        try:
            bbox_query = text(f"""
                SELECT 
                    *,
                    ST_AsGeoJSON(geom) as geometry
                FROM {layer_name}
                WHERE ST_Intersects(
                    geom,
                    ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, :srid)
                )
            """)
            
            result = db.execute(
                bbox_query,
                {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy, "srid": srid}
            )
            
            features = []
            for row in result:
                row_dict = dict(row._mapping)
                geom = row_dict.pop("geometry", None)
                features.append({
                    "type": "Feature",
                    "properties": row_dict,
                    "geometry": json.loads(geom) if geom else None
                })
            
            return features
        except Exception as e:
            logger.error(f"Error in bbox query: {e}")
            return []
    
    @staticmethod
    def query_intersect(
        db: Session,
        layer_name: str,
        geometry: Dict[str, Any],
        srid: int = 4326
    ) -> List[Dict[str, Any]]:
        """Query features that intersect with a geometry"""
        try:
            geom_json = json.dumps(geometry)
            
            intersect_query = text(f"""
                SELECT 
                    *,
                    ST_AsGeoJSON(geom) as geometry
                FROM {layer_name}
                WHERE ST_Intersects(
                    geom,
                    ST_SetSRID(ST_GeomFromGeoJSON(:geom_json), :srid)
                )
            """)
            
            result = db.execute(
                intersect_query,
                {"geom_json": geom_json, "srid": srid}
            )
            
            features = []
            for row in result:
                row_dict = dict(row._mapping)
                geom = row_dict.pop("geometry", None)
                features.append({
                    "type": "Feature",
                    "properties": row_dict,
                    "geometry": json.loads(geom) if geom else None
                })
            
            return features
        except Exception as e:
            logger.error(f"Error in intersect query: {e}")
            return []
    
    @staticmethod
    def query_buffer(
        db: Session,
        layer_name: str,
        geometry: Dict[str, Any],
        distance: float,
        srid: int = 4326
    ) -> List[Dict[str, Any]]:
        """Query features within a buffer distance of a geometry"""
        try:
            geom_json = json.dumps(geometry)
            
            # For geographic coordinates, distance should be in degrees
            # For more accurate buffer, use geography type or transform to projected CRS
            buffer_query = text(f"""
                SELECT 
                    *,
                    ST_AsGeoJSON(geom) as geometry
                FROM {layer_name}
                WHERE ST_DWithin(
                    geom,
                    ST_SetSRID(ST_GeomFromGeoJSON(:geom_json), :srid),
                    :distance
                )
            """)
            
            result = db.execute(
                buffer_query,
                {"geom_json": geom_json, "distance": distance, "srid": srid}
            )
            
            features = []
            for row in result:
                row_dict = dict(row._mapping)
                geom = row_dict.pop("geometry", None)
                features.append({
                    "type": "Feature",
                    "properties": row_dict,
                    "geometry": json.loads(geom) if geom else None
                })
            
            return features
        except Exception as e:
            logger.error(f"Error in buffer query: {e}")
            return []
    
    @staticmethod
    def query_within(
        db: Session,
        layer_name: str,
        geometry: Dict[str, Any],
        srid: int = 4326
    ) -> List[Dict[str, Any]]:
        """Query features within a polygon"""
        try:
            geom_json = json.dumps(geometry)
            
            within_query = text(f"""
                SELECT 
                    *,
                    ST_AsGeoJSON(geom) as geometry
                FROM {layer_name}
                WHERE ST_Within(
                    geom,
                    ST_SetSRID(ST_GeomFromGeoJSON(:geom_json), :srid)
                )
            """)
            
            result = db.execute(
                within_query,
                {"geom_json": geom_json, "srid": srid}
            )
            
            features = []
            for row in result:
                row_dict = dict(row._mapping)
                geom = row_dict.pop("geometry", None)
                features.append({
                    "type": "Feature",
                    "properties": row_dict,
                    "geometry": json.loads(geom) if geom else None
                })
            
            return features
        except Exception as e:
            logger.error(f"Error in within query: {e}")
            return []
    
    @staticmethod
    def get_layer_attributes(
        db: Session,
        layer_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get layer attribute information"""
        try:
            # Get column information
            columns_query = text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table_name
                AND table_schema = 'public'
            """)
            
            result = db.execute(columns_query, {"table_name": layer_name})
            
            columns = []
            for row in result:
                columns.append({
                    "name": row.column_name,
                    "type": row.data_type
                })
            
            # Get feature count
            count_query = text(f"SELECT COUNT(*) as count FROM {layer_name}")
            count_result = db.execute(count_query)
            count = count_result.scalar()
            
            return {
                "layer_name": layer_name,
                "columns": columns,
                "feature_count": count
            }
        except Exception as e:
            logger.error(f"Error getting layer attributes: {e}")
            return None


spatial_service = SpatialService()
