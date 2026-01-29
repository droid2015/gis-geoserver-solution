# Quick Start: Oracle Basemap qua GeoServer

## Tổng quan
Hướng dẫn nhanh để serve Oracle basemap tiles qua GeoServer sử dụng GeoWebCache Tile Store.

## Yêu cầu
- GeoServer đang chạy (http://localhost:8080/geoserver)
- Tiles đã được export từ Oracle và lưu tại: `geoserver_data/tiles/oracle_basemap/`

## Cấu trúc Tiles

Tiles phải được tổ chức theo format XYZ/TMS:
```
geoserver_data/tiles/oracle_basemap/
├── 10/          # Zoom level 10
│   ├── 805/     # X coordinate
│   │   ├── 499.png
│   │   ├── 500.png
│   │   └── ...
│   └── ...
├── 11/          # Zoom level 11
├── 12/
├── 13/
├── 14/
└── 15/          # Zoom level 15
```

## Các bước triển khai

### 1. Tạo file cấu hình GeoWebCache

Tạo file: `geoserver_data/gwc-layers/oracle_basemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<GeoServerTileLayer>
  <id>oracle_basemap</id>
  <enabled>true</enabled>
  <inMemoryCached>true</inMemoryCached>
  <name>oracle_basemap</name>
  <blobStoreId>defaultBlobStore</blobStoreId>
  <mimeFormats>
    <string>image/png</string>
    <string>image/jpeg</string>
  </mimeFormats>
  <gridSubsets>
    <gridSubset>
      <gridSetName>EPSG:3857</gridSetName>
      <extent>
        <coords>
          <double>11584184.5</double>
          <double>1252344.3</double>
          <double>11897270.6</double>
          <double>1565430.3</double>
        </coords>
      </extent>
      <zoomStart>10</zoomStart>
      <zoomStop>15</zoomStop>
    </gridSubset>
  </gridSubsets>
  <metaWidthHeight>
    <int>4</int>
    <int>4</int>
  </metaWidthHeight>
  <expireCache>0</expireCache>
  <expireClients>0</expireClients>
  <cacheWarningSkips>false</cacheWarningSkips>
</GeoServerTileLayer>
```

### 2. Restart GeoServer

```bash
# Nếu dùng Docker
docker-compose restart geoserver

# Hoặc từ GeoServer admin panel: Server Status → Reload
```

### 3. Verify tiles hoạt động

```bash
# Test direct tile access
curl -I "http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/10/805/499.png"

# Kiểm tra GetCapabilities
curl "http://localhost:8080/geoserver/gwc/service/wmts?REQUEST=GetCapabilities" | grep oracle_basemap
```

## URLs cho các hệ thống khác

### 1. WMS (Web Map Service) - Tiled
```
http://localhost:8080/geoserver/wms?
  SERVICE=WMS&
  VERSION=1.1.0&
  REQUEST=GetMap&
  LAYERS=oracle_basemap&
  STYLES=&
  SRS=EPSG:3857&
  BBOX={minx},{miny},{maxx},{maxy}&
  WIDTH=512&
  HEIGHT=512&
  FORMAT=image/png&
  TILED=true
```

### 2. WMTS (Web Map Tile Service)
```
http://localhost:8080/geoserver/gwc/service/wmts
```

**GetTile request:**
```
http://localhost:8080/geoserver/gwc/service/wmts?
  SERVICE=WMTS&
  REQUEST=GetTile&
  VERSION=1.0.0&
  LAYER=oracle_basemap&
  STYLE=&
  TILEMATRIXSET=EPSG:3857&
  TILEMATRIX=EPSG:3857:{z}&
  TILEROW={y}&
  TILECOL={x}&
  FORMAT=image/png
```

### 3. XYZ Tiles (TMS format) - Đơn giản nhất
```
http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/{z}/{x}/{-y}.png
```

## Sử dụng trong Frontend

### OpenLayers (hiện tại - Map.jsx)

**Option 1: Sử dụng WMS Tiled**
```javascript
import TileWMS from 'ol/source/TileWMS';

const oracleLayer = new TileLayer({
  source: new TileWMS({
    url: 'http://localhost:8080/geoserver/wms',
    params: {
      'LAYERS': 'oracle_basemap',
      'TILED': true,
      'VERSION': '1.1.0',
      'FORMAT': 'image/png'
    },
    serverType: 'geoserver',
    crossOrigin: 'anonymous'
  }),
  properties: { 
    name: 'Oracle Base Map',
    isBaseLayer: true 
  }
});
```

**Option 2: Sử dụng XYZ (Đơn giản hơn)**
```javascript
import XYZ from 'ol/source/XYZ';

const oracleLayer = new TileLayer({
  source: new XYZ({
    url: 'http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/{z}/{x}/{-y}.png',
    crossOrigin: 'anonymous'
  }),
  properties: { 
    name: 'Oracle Base Map',
    isBaseLayer: true 
  }
});
```

### Leaflet
```javascript
var oracleLayer = L.tileLayer.wms('http://localhost:8080/geoserver/wms', {
  layers: 'oracle:oracle_basemap',
  format: 'image/png',
  transparent: false,
  tiled: true,
  attribution: 'Oracle Basemap'
});
```

### MapLibre/Mapbox
```javascript
map.addSource('oracle-basemap', {
  type: 'raster',
  tiles: [
    'http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle:oracle_basemap@EPSG:3857@png/{z}/{x}/{y}.png'
  ],
  tileSize: 256
});

map.addLayer({
  id: 'oracle-basemap-layer',
  type: 'raster',
  source: 'oracle-basemap'
});
```

## Export Tiles từ Oracle (Tham khảo)

**⚠️ Lưu ý bảo mật:** Thông tin kết nối Oracle không được commit vào repository.

### Yêu cầu:
- Python 3.8+
- cx_Oracle hoặc oracledb driver  
- Quyền truy cập Oracle database (BANDONEN table)

### Cấu trúc BANDONEN table:
```sql
-- Table structure
TYPE   NUMBER   -- 1=png, 2=jpg, 3=jpeg, 4=webp
X      NUMBER   -- Tile X coordinate
Y      NUMBER   -- Tile Y coordinate  
ZOOM   NUMBER   -- Zoom level (10-15)
TILE   BLOB     -- Tile image data
```

### Script export (không chứa connection info):
```python
# Sử dụng scripts/export_oracle_tiles.py
# Configure connection trong .env.local (NOT committed to git)
python export_oracle_tiles.py
```

Output sẽ tạo tiles tại: `geoserver_data/tiles/oracle_basemap/`

## Troubleshooting

### Tiles không hiển thị
```bash
# 1. Kiểm tra file tiles tồn tại
ls geoserver_data/tiles/oracle_basemap/10/805/

# 2. Kiểm tra GeoServer logs
tail -f geoserver_data/logs/geoserver.log

# 3. Test direct tile access
curl -I http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/10/805/499.png
```

### File cấu hình không load
- Verify XML syntax trong `gwc-layers/oracle_basemap.xml`
- Restart GeoServer sau khi thay đổi config
- Check file permissions

### CORS errors
```xml
<!-- Thêm vào geoserver_data/web.xml nếu cần -->
<filter>
  <filter-name>CorsFilter</filter-name>
  <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
  <init-param>
    <param-name>cors.allowed.origins</param-name>
    <param-value>*</param-value>
  </init-param>
</filter>
```

## Performance Tips

1. **Static tiles:** Tiles đã được tạo sẵn, performance tốt
2. **Use SSD:** Mount tiles directory trên SSD nếu có thể
3. **Configure cache:** Tăng cache size trong GeoServer nếu cần
4. **Use CDN:** Deploy với CDN nếu publish ra internet

## Security

✅ **Biện pháp bảo mật đã áp dụng:**
- Không lưu thông tin Oracle connection trong repository
- Sử dụng pre-generated tiles - không cần database connection khi serving  
- Tiles static - giảm attack surface

🔒 **Nếu deploy production:**
1. Thay đổi password GeoServer admin
2. Cấu hình firewall
3. Enable HTTPS (SSL/TLS)
4. Restrict IP access nếu cần
5. Setup authentication cho WMS/WMTS
6. Sử dụng reverse proxy (nginx, Apache)

## Next Steps

- [ ] Verify tiles hoạt động trong frontend
- [ ] Test performance với nhiều concurrent requests
- [ ] Setup monitoring và logging
- [ ] Configure CDN nếu deploy ra internet
- [ ] Backup tiles directory định kỳ

