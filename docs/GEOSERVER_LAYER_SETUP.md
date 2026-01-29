# Hướng dẫn tạo Layer Oracle Basemap trong GeoServer

## Phương án 1: Sử dụng Script tự động (Khuyến nghị)

### Trên Windows:
```cmd
cd scripts
setup_geoserver_layer.bat
```

Script sẽ tự động:
- Tạo workspace `basemap`
- Tạo Coverage Store `oracle_tiles`
- Publish layer `oracle_basemap`
- Enable tile caching với EPSG:3857

## Phương án 2: Cấu hình thủ công qua Web UI

### 1. Đăng nhập GeoServer
- URL: http://localhost:8080/geoserver
- User: admin / Pass: geoserver

### 2. Tạo Workspace
- **Data** → **Workspaces** → **Add new workspace**
- Name: `basemap`
- Namespace URI: `http://basemap`
- ✓ Default Workspace
- Click **Submit**

### 3. Tạo Store

#### Option A: ImageMosaic (cho nhiều tiles)
- **Data** → **Stores** → **Add new Store**
- **Raster Data Sources** → **ImageMosaic**
- Workspace: `basemap`
- Data Source Name: `oracle_tiles`
- URL: `file:///opt/geoserver/data_dir/tiles/oracle_basemap`
- Click **Save**

#### Option B: GeoTIFF (nếu merge thành 1 file)
- **Data** → **Stores** → **Add new Store**
- **Raster Data Sources** → **GeoTIFF**
- URL: đường dẫn đến file tiff

### 4. Publish Layer
- **Data** → **Layers** → **Add a new layer**
- Choose Store: `basemap:oracle_tiles`
- Click **Publish** trên layer xuất hiện
- Configure:
  - **Name**: `oracle_basemap`
  - **Title**: Oracle Basemap
  - **Declared SRS**: EPSG:3857 (hoặc EPSG:4326)
  - Click **Compute from data** ở Native Bounding Box
  - Click **Compute from native bounds** ở Lat/Lon Bounding Box
- Tab **Tile Caching**:
  - ✓ Create a cached layer for this layer
  - Tile image formats: PNG, JPEG
  - Gridsets: EPSG:3857, EPSG:4326
- Click **Save**

### 5. Seed Tiles (Optional)
- **Tile Caching** → **Tile Layers**
- Tìm layer `basemap:oracle_basemap`
- Click **Seed/Truncate**
- Configure:
  - Number of tasks: 4
  - Type of operation: Seed
  - Grid Set: EPSG:3857
  - Format: image/png
  - Zoom start: 1
  - Zoom stop: 18
- Click **Submit**

## Phương án 3: Tạo Pyramid Tiles (Advanced)

### Tạo tile index với GDAL
```bash
# Trên host machine
cd geoserver_data/tiles/oracle_basemap

# Tạo VRT cho mỗi zoom level
for z in {1..18}; do
  gdalbuildvrt -resolution user -tr 256 256 \
    zoom_${z}.vrt ${z}/*/*.png
done

# Merge tất cả VRT
gdalbuildvrt -resolution user oracle_basemap.vrt zoom_*.vrt
```

Sau đó publish VRT file trong GeoServer như GeoTIFF.

## Testing

### 1. Layer Preview
- **Data** → **Layer Preview**
- Tìm `basemap:oracle_basemap`
- Click **OpenLayers**

### 2. WMS GetMap Request
```
http://localhost:8080/geoserver/basemap/wms?
  service=WMS&
  version=1.1.0&
  request=GetMap&
  layers=basemap:oracle_basemap&
  bbox=102.0,8.0,110.0,24.0&
  width=768&
  height=768&
  srs=EPSG:4326&
  format=image/png
```

### 3. WMTS GetTile Request
```
http://localhost:8080/geoserver/gwc/service/wmts?
  REQUEST=GetTile&
  SERVICE=WMTS&
  VERSION=1.0.0&
  LAYER=basemap:oracle_basemap&
  STYLE=&
  TILEMATRIXSET=EPSG:3857&
  TILEMATRIX=EPSG:3857:13&
  TILEROW=3858&
  TILECOL=6509&
  FORMAT=image/png
```

## Sử dụng trong Frontend

### Cập nhật App.jsx để dùng GeoServer layer

```javascript
const loadOracleBasemap = () => {
  setMapLayers((prev) => [
    ...prev.filter((l) => l.name !== 'oracle_basemap'),
    {
      name: 'oracle_basemap',
      type: 'wms',  // Hoặc 'wmts'
      layers: 'basemap:oracle_basemap',
      url: 'http://localhost:8080/geoserver/wms',
      visible: true,
      opacity: 1.0,
      isBaseLayer: true
    },
  ]);
};
```

### Hoặc dùng WMTS (hiệu năng tốt hơn)

```javascript
import WMTS from 'ol/source/WMTS';
import WMTSTileGrid from 'ol/tilegrid/WMTS';
import { get as getProjection } from 'ol/proj';
import { getTopLeft, getWidth } from 'ol/extent';

const projection = getProjection('EPSG:3857');
const projectionExtent = projection.getExtent();
const size = getWidth(projectionExtent) / 256;
const resolutions = new Array(19);
const matrixIds = new Array(19);

for (let z = 0; z < 19; ++z) {
  resolutions[z] = size / Math.pow(2, z);
  matrixIds[z] = 'EPSG:3857:' + z;
}

const oracleBasemap = new TileLayer({
  source: new WMTS({
    url: 'http://localhost:8080/geoserver/gwc/service/wmts',
    layer: 'basemap:oracle_basemap',
    matrixSet: 'EPSG:3857',
    format: 'image/png',
    projection: projection,
    tileGrid: new WMTSTileGrid({
      origin: getTopLeft(projectionExtent),
      resolutions: resolutions,
      matrixIds: matrixIds
    }),
    style: '',
    wrapX: true
  })
});
```

## Troubleshooting

### Lỗi: No data found
- Kiểm tra tiles có trong container: `docker exec gis-geoserver ls -la /opt/geoserver/data_dir/tiles/oracle_basemap/`
- Kiểm tra quyền truy cập files

### Lỗi: Could not find coverage
- Đảm bảo store type đúng (ImageMosaic cho tiles structure)
- Kiểm tra đường dẫn URL chính xác

### Lỗi: Rendering failed
- Kiểm tra SRS/CRS phù hợp với data
- Verify bounding box đúng
- Check tile coordinate system (TMS vs XYZ)

### Performance Issues
- Enable direct raster rendering
- Increase memory: INITIAL_MEMORY, MAXIMUM_MEMORY
- Use tile caching (GeoWebCache)
- Consider using MrSID or ECW format cho large rasters
