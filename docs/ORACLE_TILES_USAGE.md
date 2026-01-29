# Hướng dẫn sử dụng Oracle Basemap Tiles trong GeoServer

## Tiles đã được export và copy vào:
`geoserver_data/tiles/oracle_basemap/`

Cấu trúc: `{zoom}/{x}/{y}.png`
- Zoom levels: 1-18
- Format: PNG

## Cách 1: Sử dụng TMS/WMTS Service (Đơn giản nhất)

### 1. Truy cập vào GeoServer container
```bash
docker exec -it gis-geoserver bash
```

### 2. Kiểm tra tiles đã có
```bash
ls -la /opt/geoserver/data_dir/tiles/oracle_basemap/
```

### 3. Cấu hình Gridset trong GeoServer Web UI

a. Đăng nhập: http://localhost:8080/geoserver
   - User: admin
   - Pass: geoserver

b. **Tile Caching** → **Gridsets** → **Add a new gridset**
   - Name: `ORACLE_GRID`
   - SRS: `EPSG:3857` (hoặc `EPSG:4326` tùy tile scheme)
   - Tile dimensions: 256x256
   - Zoom levels: 1-18
   - Click **Save**

### 4. Cấu hình Blob Store

a. **Tile Caching** → **Blob Stores** → **Add new blob store**
   - Type: `File system`
   - ID: `oracle_basemap`
   - Base directory: `/opt/geoserver/data_dir/tiles/oracle_basemap`
   - Click **Save**

### 5. Tạo Layer từ Tiles

**Option A: Tạo Tile Layer trực tiếp**
- **Tile Caching** → **Tile Layers** → **Add new layer**
- Chọn blob store: `oracle_basemap`
- Gridset: `ORACLE_GRID`
- Format: `image/png`

**Option B: Publish qua Coverage Store**
- **Data** → **Stores** → **Add new Store**
- **Other Sources** → **GeoTIFF** (hoặc World Image nếu có)

## Cách 2: Sử dụng REST API để cấu hình

### Script tự động cấu hình
```bash
# Chạy từ host machine
docker exec gis-geoserver bash -c "curl -u admin:geoserver -X POST \
  'http://localhost:8080/geoserver/rest/workspaces' \
  -H 'Content-Type: application/json' \
  -d '{\"workspace\":{\"name\":\"basemap\"}}'"
```

## Cách 3: Serve tiles qua HTTP trực tiếp

### Sửa docker-compose.yml để serve tiles
Thêm nginx service để serve tiles:

```yaml
nginx-tiles:
  image: nginx:alpine
  container_name: tile-server
  volumes:
    - ./geoserver_data/tiles/oracle_basemap:/usr/share/nginx/html/tiles
  ports:
    - "8081:80"
  networks:
    - gis-network
```

Tiles sẽ accessible tại: `http://localhost:8081/tiles/{z}/{x}/{y}.png`

## Sử dụng trong Frontend

### Option 1: XYZ Tiles (Direct HTTP)
```javascript
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';

const oracleBasemap = new TileLayer({
  source: new XYZ({
    url: 'http://localhost:8081/tiles/{z}/{x}/{y}.png',
    maxZoom: 18,
    minZoom: 1
  })
});
```

### Option 2: TMS từ GeoServer
```javascript
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';

const oracleBasemap = new TileLayer({
  source: new TileWMS({
    url: 'http://localhost:8080/geoserver/gwc/service/tms/1.0.0',
    params: {
      'LAYERS': 'oracle_basemap'
    }
  })
});
```

## Testing

Test URL trực tiếp:
- Zoom 1: `http://localhost:8081/tiles/1/1/1.png`
- Zoom 13: `http://localhost:8081/tiles/13/6509/3858.png`

## Troubleshooting

### Lỗi: 404 Not Found
- Kiểm tra tiles có trong container: `docker exec gis-geoserver ls /opt/geoserver/data_dir/tiles/`
- Volume mapping trong docker-compose.yml đúng chưa

### Lỗi: Tiles không hiển thị
- Kiểm tra coordinate system (EPSG)
- Kiểm tra zoom levels phù hợp với data
- Verify tile naming scheme: {z}/{x}/{y}.png

### Performance
- Nếu tiles nhiều, consider using CDN
- Enable browser caching
- Compress PNG tiles nếu cần
