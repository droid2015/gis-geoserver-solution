# Hướng dẫn sử dụng bản đồ nền từ Oracle trong GeoServer

## Phương án 1: Export tiles ra filesystem (Đơn giản nhất)

### 1. Cài đặt thư viện Oracle
```bash
pip install oracledb
```

### 2. Chạy script export
```bash
# Export ra cấu trúc thư mục tiles
python scripts/export_oracle_tiles.py

# Hoặc export ra MBTiles format
python scripts/export_oracle_tiles.py mbtiles
```

### 3. Cấu hình trong GeoServer

#### Option A: Sử dụng tiles từ filesystem
1. Copy thư mục `tiles_output` vào `geoserver_data/tiles/`
2. Cấu hình WMTS layer trong GeoServer:
   - **Data** → **Tile Layers** → **Add new layer**
   - Chọn **Tile cache directory**: `${GEOSERVER_DATA_DIR}/tiles/tiles_output`

#### Option B: Sử dụng MBTiles
1. Cài đặt **MBTiles plugin** cho GeoServer:
   - Download từ: https://geoserver.org/release/stable/
   - Copy JAR files vào: `geoserver/WEB-INF/lib/`
   - Restart GeoServer

2. Trong GeoServer:
   - **Data** → **Stores** → **Add new Store**
   - Chọn **MBTiles**
   - **Connection Parameters**: 
     - Database: `file:geoserver_data/tiles/basemap.mbtiles`
   - **Save**

3. Publish layer:
   - **Data** → **Layers** → **Add new layer**
   - Chọn store MBTiles vừa tạo
   - Publish layer

## Phương án 2: Kết nối trực tiếp Oracle (Advanced)

### 1. Tạo custom tile source trong GeoWebCache

Tạo file: `geoserver_data/gwc/oracle-tile-source.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<blobStore>
  <id>oracle-blob-store</id>
  <enabled>true</enabled>
  <default>false</default>
  <jdbcConfiguration>
    <dialect>Oracle</dialect>
    <JDBCUrl>jdbc:oracle:thin:@localhost:1521:ORCL</JDBCUrl>
    <username>DOXASPC</username>
    <password>your_password</password>
    <tableNamePrefix>BANDONEN</tableNamePrefix>
  </jdbcConfiguration>
</blobStore>
```

### 2. Cấu hình mapping trong GeoServer

Cần tạo custom plugin hoặc sử dụng GeoWebCache REST API.

## Phương án 3: Chuyển sang PostGIS (Khuyến nghị cho tích hợp tốt)

### 1. Export Oracle data sang PostGIS

```sql
-- Tạo bảng trong PostGIS
CREATE TABLE basemap_tiles (
    type INTEGER,
    x INTEGER,
    y INTEGER,
    zoom INTEGER,
    tile BYTEA,
    PRIMARY KEY (zoom, x, y)
);

CREATE INDEX idx_basemap_zoom ON basemap_tiles(zoom);
CREATE INDEX idx_basemap_xy ON basemap_tiles(x, y);
```

### 2. Script chuyển dữ liệu từ Oracle sang PostGIS

Sử dụng script Python để migrate data.

### 3. Cấu hình trong GeoServer

Sử dụng PostGIS Tile Store hoặc setup WMTS từ PostGIS.

## Sử dụng trong Frontend

Sau khi cấu hình xong GeoServer, thêm vào frontend:

```javascript
// Trong App.jsx
const loadOracleBasemap = () => {
  setMapLayers((prev) => [
    ...prev,
    {
      name: 'oracle_basemap',
      type: 'wms',
      layers: 'oracle_basemap',
      url: 'http://localhost:8080/geoserver/gwc/service/wms',
      visible: true,
      opacity: 1.0,
      isBaseLayer: true
    }
  ]);
};
```

## Khuyến nghị

**Dùng Phương án 1 với MBTiles** vì:
- Đơn giản, dễ triển khai
- Hiệu năng tốt
- Tương thích tốt với GeoServer
- Dễ backup và di chuyển

Hãy chọn phương án phù hợp với nhu cầu của bạn!
