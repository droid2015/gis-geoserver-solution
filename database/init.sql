-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;

-- Create layers metadata table
CREATE TABLE IF NOT EXISTS layers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255),
    description TEXT,
    geometry_type VARCHAR(50),
    srid INTEGER DEFAULT 4326,
    bbox GEOMETRY(Polygon, 4326),
    style VARCHAR(255),
    visible BOOLEAN DEFAULT true,
    opacity FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_layers_name ON layers(name);

-- Create sample data: Vietnam cities
CREATE TABLE IF NOT EXISTS vietnam_cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    population INTEGER,
    description TEXT,
    type VARCHAR(50),
    geom GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vietnam_cities_geom ON vietnam_cities USING GIST(geom);

-- Insert sample cities
INSERT INTO vietnam_cities (name, name_en, population, type, geom) VALUES
    ('Hà Nội', 'Hanoi', 8000000, 'Capital', ST_SetSRID(ST_MakePoint(105.8342, 21.0278), 4326)),
    ('TP Hồ Chí Minh', 'Ho Chi Minh City', 9000000, 'City', ST_SetSRID(ST_MakePoint(106.6297, 10.8231), 4326)),
    ('Đà Nẵng', 'Da Nang', 1200000, 'City', ST_SetSRID(ST_MakePoint(108.2022, 16.0544), 4326)),
    ('Hải Phòng', 'Hai Phong', 2000000, 'City', ST_SetSRID(ST_MakePoint(106.6881, 20.8449), 4326)),
    ('Cần Thơ', 'Can Tho', 1200000, 'City', ST_SetSRID(ST_MakePoint(105.7467, 10.0452), 4326)),
    ('Huế', 'Hue', 340000, 'Province Capital', ST_SetSRID(ST_MakePoint(107.5955, 16.4637), 4326)),
    ('Nha Trang', 'Nha Trang', 400000, 'City', ST_SetSRID(ST_MakePoint(109.1967, 12.2388), 4326)),
    ('Vũng Tàu', 'Vung Tau', 450000, 'City', ST_SetSRID(ST_MakePoint(107.0843, 10.3460), 4326)),
    ('Quy Nhơn', 'Quy Nhon', 280000, 'City', ST_SetSRID(ST_MakePoint(109.2189, 13.7830), 4326)),
    ('Buôn Ma Thuột', 'Buon Ma Thuot', 340000, 'Province Capital', ST_SetSRID(ST_MakePoint(108.0378, 12.6726), 4326));

-- Function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_layers_updated_at BEFORE UPDATE ON layers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert initial layer metadata for vietnam_cities
INSERT INTO layers (name, title, description, geometry_type, srid, visible, opacity)
VALUES ('vietnam_cities', 'Các thành phố Việt Nam', 'Sample data - Vietnam cities with population', 'Point', 4326, true, 1.0)
ON CONFLICT (name) DO NOTHING;
