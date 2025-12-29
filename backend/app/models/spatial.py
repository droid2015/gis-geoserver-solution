from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, Date
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.database import Base


class Layer(Base):
    """Layer metadata model"""
    __tablename__ = "layers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(255))
    description = Column(Text)
    geometry_type = Column(String(50))
    srid = Column(Integer, default=4326)
    bbox = Column(Geometry('POLYGON', srid=4326))
    style = Column(String(255))
    visible = Column(Boolean, default=True)
    opacity = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class VietnamCity(Base):
    """Vietnam cities sample data model"""
    __tablename__ = "vietnam_cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255))
    population = Column(Integer)
    description = Column(Text)
    type = Column(String(50))
    geom = Column(Geometry('POINT', srid=4326))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Highway(Base):
    """Highways model"""
    __tablename__ = "highways"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255))
    type = Column(String(100))
    length_km = Column(Float)
    lanes = Column(Integer)
    max_speed = Column(Integer)
    status = Column(String(50))
    start_point = Column(String(255))
    end_point = Column(String(255))
    opened_date = Column(Date)
    description = Column(Text)
    geom = Column(Geometry('LINESTRING', srid=4326))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
