from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class LayerBase(BaseModel):
    """Base schema for layer"""
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    geometry_type: Optional[str] = None
    srid: int = 4326
    style: Optional[str] = None
    visible: bool = True
    opacity: float = 1.0


class LayerCreate(LayerBase):
    """Schema for creating a layer"""
    pass


class LayerUpdate(BaseModel):
    """Schema for updating a layer"""
    title: Optional[str] = None
    description: Optional[str] = None
    style: Optional[str] = None
    visible: Optional[bool] = None
    opacity: Optional[float] = None


class LayerResponse(LayerBase):
    """Schema for layer response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class FeatureBase(BaseModel):
    """Base schema for feature"""
    properties: Dict[str, Any]
    geometry: Optional[Dict[str, Any]] = None


class FeatureResponse(FeatureBase):
    """Schema for feature response"""
    id: int
    
    class Config:
        from_attributes = True


class BBoxQuery(BaseModel):
    """Schema for bounding box query"""
    layer_name: str
    minx: float
    miny: float
    maxx: float
    maxy: float
    srid: int = 4326


class BufferQuery(BaseModel):
    """Schema for buffer query"""
    layer_name: str
    geometry: Dict[str, Any]
    distance: float
    srid: int = 4326


class IntersectQuery(BaseModel):
    """Schema for intersection query"""
    layer_name: str
    geometry: Dict[str, Any]
    srid: int = 4326


class WithinQuery(BaseModel):
    """Schema for within query"""
    layer_name: str
    geometry: Dict[str, Any]
    srid: int = 4326


class UploadResponse(BaseModel):
    """Schema for upload response"""
    success: bool
    message: str
    layer_name: Optional[str] = None
    feature_count: Optional[int] = None
    errors: Optional[List[str]] = None
