# Hướng dẫn Publish Oracle Basemap qua GeoServer

## Tổng quan
Tài liệu này hướng dẫn cách publish Oracle basemap tiles qua GeoServer để các hệ thống khác có thể sử dụng thông qua WMS/WMTS.

**Phương án được sử dụng:** GeoWebCache với Tile Store (Pre-generated tiles)

## Ưu điểm phương án này:
- ✅ Hiệu suất cao - tiles đã được tạo sẵn
- ✅ Bảo mật - không cần expose kết nối Oracle
- ✅ Độc lập - không phụ thuộc vào Oracle database khi serving
- ✅ Dễ scale - có thể dùng CDN, load balancer

## Hướng dẫn triển khai

### Bước 1: Chuẩn bị tiles từ Oracle

Tiles đã được export từ Oracle và lưu tại:
```
geoserver_data/tiles/oracle_basemap/
```

Cấu trúc thư mục:
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

### Bước 2: Cấu hình GeoWebCache Tile Store

Tạo file cấu hình: `geoserver_data/gwc-layers/oracle_basemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<GeoServerTileLayer>
  <id>oracle_basemap</id>
  <enabled>true</enabled>
  <inMemoryCached>true</inMemoryCached>
  <name>oracle_basemap</name>
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

### Bước 3: Restart GeoServer

Sau khi tạo file cấu hình, restart GeoServer:
```bash
# Nếu dùng Docker
docker-compose restart geoserver

# Hoặc từ GeoServer admin panel
# Server Status → Reload → Submit
```

### Bước 4: Truy cập tiles qua GeoServer

Sau khi restart, tiles có thể truy cập qua:

**WMTS:**
```
http://localhost:8080/geoserver/gwc/service/wmts?
  REQUEST=GetTile&
  SERVICE=WMTS&
  VERSION=1.0.0&
  LAYER=oracle_basemap&
  STYLE=&
  TILEMATRIXSET=EPSG:3857&
  TILEMATRIX=EPSG:3857:{z}&
  TILEROW={y}&
  TILECOL={x}&
  FORMAT=image/png
```

**TMS:**
```
http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/{z}/{x}/{y}.png
```

**XYZ (OpenLayers format):**
```
http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle_basemap@EPSG:3857@png/{z}/{x}/{-y}.png
```

## Phương pháp Export Tiles từ Oracle

**Lưu ý bảo mật:** Thông tin kết nối Oracle không được lưu trong repository.

### Cách export tiles:

1. Sử dụng script `scripts/export_oracle_tiles.py` (không commit thông tin connection)
2. Hoặc export trực tiếp từ Oracle database
3. Tiles được export theo format: `{zoom}/{x}/{y}.png`
4. Lưu vào: `geoserver_data/tiles/oracle_basemap/`

### Requirements cho export:
- Python 3.8+
- cx_Oracle hoặc oracledb driver
- Quyền truy cập Oracle database (BANDONEN table)
- Zoom levels: 10-15

## Cập nhật Frontend

Sau khi publish, cập nhật Map.jsx để sử dụng GeoServer tiles:

```javascript
// Thay vì:
url: 'http://localhost:8081/tiles/oracle_basemap/{z}/{x}/{y}.png'

// Sử dụng GeoServer WMTS:
import WMTS from 'ol/source/WMTS';
import WMTSTileGrid from 'ol/tilegrid/WMTS';

const projection = getProjection('EPSG:3857');
const projectionExtent = projection.getExtent();
const size = getWidth(projectionExtent) / 256;
const resolutions = new Array(6); // zoom 10-15
const matrixIds = new Array(6);

for (let z = 0; z < 6; ++z) {
  resolutions[z] = size / Math.pow(2, z + 10);
  matrixIds[z] = 'EPSG:3857:' + (z + 10);
}

const oracleLayer = new TileLayer({
  source: new WMTS({
    url: 'http://localhost:8080/geoserver/gwc/service/wmts',
    layer: 'oracle_basemap',
    matrixSet: 'EPSG:3857',
    format: 'image/png',
    projection: projection,
    tileGrid: new WMTSTileGrid({
      origin: getTopLeft(projectionExtent),
      resolutions: resolutions,
      matrixIds: matrixIds,
    }),
    style: '',
  }),
  properties: { 
    name: 'Oracle Base Map',
    isBaseLayer: true 
  }
});

// Hoặc sử dụng TileWMS với TILED=true:
const oracleLayer = new TileLayer({
  source: new TileWMS({
    url: 'http://localhost:8080/geoserver/wms',
    params: {
      'LAYERS': 'oracle:oracle_basemap',
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

## Thông tin kỹ thuật

| Thông số | Giá trị |
|----------|----------|
| **Tile Format** | PNG (image/png) |
| **Projection** | EPSG:3857 (Web Mercator) |
| **Zoom Levels** | 10-15 |
| **Tile Size** | 256x256 pixels |
| **Storage** | File system (geoserver_data/tiles/) |

## Các URLs có thể sử dụng

Sau khi publish, các hệ thống khác có thể truy cập qua:

1. **WMS GetCapabilities:**
   ```
   http://localhost:8080/geoserver/oracle/wms?service=WMS&request=GetCapabilities
   ```

2. **WMTS GetCapabilities:**
   ```
   http://localhost:8080/geoserver/gwc/service/wmts?REQUEST=GetCapabilities
   ```

3. **Direct Tile Access (XYZ):**
   ```
   http://localhost:8080/geoserver/gwc/service/tms/1.0.0/oracle:oracle_basemap@EPSG:3857@png/{z}/{x}/{-y}.png
   ```

## Lưu ý bảo mật

### ✅ Các biện pháp đã áp dụng:
1. **Không lưu thông tin Oracle connection** trong repository
2. **Sử dụng pre-generated tiles** - không cần kết nối database khi serving
3. **Tiles static** - giảm attack surface

### 🔒 Nếu publish ra internet:
1. Cấu hình authentication cho GeoServer admin panel
2. Sử dụng HTTPS (SSL/TLS)
3. Hạn chế IP access nếu cần
4. Cấu hình rate limiting
5. Sử dụng reverse proxy (nginx, Apache)
6. Enable firewall rules

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

### Performance chậm
- Tiles đã static nên performance nên tốt
- Nếu vẫn chậm: check disk I/O
- Consider mounting tiles directory on SSD
- Use CDN for internet-facing deployments

### CORS errors
```xml
<!-- Thêm vào geoserver_data/web.xml -->
<filter>
  <filter-name>CorsFilter</filter-name>
  <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
  <init-param>
    <param-name>cors.allowed.origins</param-name>
    <param-value>*</param-value>
  </init-param>
</filter>
```
