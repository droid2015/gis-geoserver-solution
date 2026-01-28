"""
Export tiles from Oracle BANDONEN table to filesystem for GeoServer/GeoWebCache
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Result

# Load environment variables
load_dotenv('.env.oracle')

# Build Oracle connection string
def get_connection_string() -> str:
    """Build Oracle connection string for SQLAlchemy"""
    user = os.getenv('ORACLE_USER', 'DOXASPC')
    password = os.getenv('ORACLE_PASSWORD', 'your_password')
    host = os.getenv('ORACLE_HOST', 'localhost')
    port = os.getenv('ORACLE_PORT', '1521')
    service = os.getenv('ORACLE_SERVICE', 'ORCL')
    
    return f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"

# Create SQLAlchemy engine
def create_oracle_engine() -> Engine:
    """Create SQLAlchemy engine for Oracle database"""
    connection_string = get_connection_string()
    return create_engine(connection_string, echo=False)

# Output directory for tiles
OUTPUT_DIR = os.getenv('OUTPUT_DIR', './tiles_output')

def get_tile_extension(tile_type):
    """Get file extension based on tile type"""
    extensions = {
        1: 'png',
        2: 'jpg',
        3: 'jpeg',
        4: 'webp'
    }
    return extensions.get(tile_type, 'png')

def export_tiles():
    """Export tiles from Oracle to filesystem in TMS/XYZ format"""
    
    # Create engine and connect
    engine = create_oracle_engine()
    
    print("Exporting tiles from Oracle...")
    
    # Query all tiles
    query = text("""
        SELECT TYPE, X, Y, ZOOM, TILE 
        FROM BANDONEN 
        ORDER BY ZOOM, Y, X
    """)
    
    tile_count = 0
    
    with engine.connect() as connection:
        result: Result = connection.execute(query)
        
        for row in result:
            tile_type, x, y, zoom, tile_blob = row
            
            # Create directory structure: tiles/{zoom}/{x}/{y}.png
            tile_dir = os.path.join(OUTPUT_DIR, str(zoom), str(x))
            Path(tile_dir).mkdir(parents=True, exist_ok=True)
            
            # Determine file extension based on type
            extension = get_tile_extension(tile_type)
            tile_path = os.path.join(tile_dir, f"{y}.{extension}")
            
            # Write tile to file
            if tile_blob:
                with open(tile_path, 'wb') as f:
                    f.write(tile_blob)
                tile_count += 1
                
                if tile_count % 1000 == 0:
                    print(f"Exported {tile_count} tiles...")
    
    print(f"Export completed! Total tiles: {tile_count}")
    print(f"Tiles saved to: {OUTPUT_DIR}")

def export_to_mbtiles():
    """Export tiles from Oracle to MBTiles format"""
    import sqlite3
    
    # Create engine
    engine = create_oracle_engine()
    
    # Create MBTiles database
    mbtiles_path = os.path.join(OUTPUT_DIR, 'basemap.mbtiles')
    mbtiles_conn = sqlite3.connect(mbtiles_path)
    mbtiles_cursor = mbtiles_conn.cursor()
    
    # Create MBTiles schema
    mbtiles_cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            name TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    mbtiles_cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiles (
            zoom_level INTEGER,
            tile_column INTEGER,
            tile_row INTEGER,
            tile_data BLOB,
            PRIMARY KEY (zoom_level, tile_column, tile_row)
        )
    ''')
    
    # Insert metadata
    metadata = [
        ('name', 'Oracle Basemap'),
        ('type', 'baselayer'),
        ('version', '1.0'),
        ('description', 'Basemap from Oracle'),
        ('format', 'png'),
        ('bounds', '-180,-85,180,85')
    ]
    mbtiles_cursor.executemany(
        'INSERT OR REPLACE INTO metadata (name, value) VALUES (?, ?)',
        metadata
    )
    
    print("Exporting to MBTiles format...")
    
    # Query and insert tiles
    query = text("SELECT X, Y, ZOOM, TILE FROM BANDONEN ORDER BY ZOOM, Y, X")
    
    tile_count = 0
    
    with engine.connect() as connection:
        result: Result = connection.execute(query)
        
        for row in result:
            x, y, zoom, tile_blob = row
            
            # MBTiles uses TMS scheme (Y axis flipped)
            tms_y = (2 ** zoom) - 1 - y
            
            if tile_blob:
                mbtiles_cursor.execute(
                    'INSERT OR REPLACE INTO tiles (zoom_level, tile_column, tile_row, tile_data) VALUES (?, ?, ?, ?)',
                    (zoom, x, tms_y, tile_blob)
                )
                tile_count += 1
                
                if tile_count % 1000 == 0:
                    print(f"Exported {tile_count} tiles...")
                    mbtiles_conn.commit()
    
    mbtiles_conn.commit()
    mbtiles_cursor.close()
    mbtiles_conn.close()
    
    print(f"MBTiles export completed! Total tiles: {tile_count}")
    print(f"File saved to: {mbtiles_path}")

if __name__ == '__main__':
    import sys
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'mbtiles':
        export_to_mbtiles()
    else:
        export_tiles()
