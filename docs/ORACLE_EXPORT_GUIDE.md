# Hướng dẫn Export Tiles từ Oracle sang GeoServer (MBTiles)

## Bước 1: Cấu hình kết nối Oracle

Sửa file `scripts/.env.oracle`:

```properties
ORACLE_USER=DOXASPC
ORACLE_PASSWORD=your_actual_password
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=ORCL
OUTPUT_DIR=./tiles_output
```

## Bước 2: Chạy script export

### Trên Windows:
```cmd
cd scripts
run_export.bat
```

### Hoặc chạy trực tiếp:
```cmd
cd scripts
python export_oracle_tiles.py mbtiles
```

Script sẽ:
- Kết nối đến Oracle database
- Đọc tất cả tiles từ bảng BANDONEN
- Export sang file MBTiles: `tiles_output/basemap.mbtiles`

## Bước 3: Copy MBTiles vào GeoServer

```cmd
# Tạo thư mục tiles trong geoserver_data
mkdir geoserver_data\tiles

# Copy file MBTiles
copy scripts\tiles_output\basemap.mbtiles geoserver_data\tiles\
```

## Bước 4: Cài đặt MBTiles Plugin cho GeoServer

### Cách 1: Download plugin (Khuyến nghị)

1. Vào https://geoserver.org/release/stable/
2. Download **GeoServer 2.28.0**
3. Tìm và download: **MBTiles Extension**
4. Giải nén và copy tất cả file JAR vào: `geoserver/WEB-INF/lib/`
5. Restart GeoServer container:
   ```cmd
   docker-compose restart geoserver
   ```

### Cách 2: Tự động cài đặt trong Docker

Sửa Dockerfile cho GeoServer để tự động cài plugin.

## Bước 5: Cấu hình trong GeoServer

1. **Đăng nhập GeoServer**: http://localhost:8080/geoserver (admin/geoserver)

2. **Tạo Store**:
   - **Data** → **Stores** → **Add new Store**
   - Chọn **MBTiles** (nếu có plugin)
   - Điền thông tin:
     - **Workspace**: Chọn `vietnam_data` hoặc tạo mới
     - **Data Source Name**: `oracle_basemap`
     - **Database**: `/opt/geoserver/data_dir/tiles/basemap.mbtiles`
   - Click **Save**

3. **Publish Layer**:
   - **Data** → **Layers** → **Add new layer**
   - Chọn **Store**: `oracle_basemap`
   - Click **Publish**
   - Cấu hình:
     - **Title**: Oracle Basemap
     - **Compute from data** để set bounds
     - **Tile Caching**: Enable
   - Click **Save**

## Bước 6: Sử dụng trong Frontend

Layer sẽ tự động xuất hiện qua WMTS/TMS endpoint:
- WMTS: `http://localhost:8080/geoserver/gwc/service/wmts`
- TMS: `http://localhost:8080/geoserver/gwc/service/tms/1.0.0`

Frontend đã được cấu hình sẵn để load layer này.

## Kiểm tra

Test layer trong GeoServer:
- **Data** → **Layer Preview**
- Tìm layer `oracle_basemap`
- Click **OpenLayers** để xem preview

## Troubleshooting

### Lỗi: Không tìm thấy MBTiles Store
- Kiểm tra plugin đã cài đúng chưa
- Restart GeoServer sau khi cài plugin

### Lỗi: Không kết nối được Oracle
- Kiểm tra thông tin trong `.env.oracle`
- Đảm bảo Oracle database đang chạy
- Test kết nối với SQL*Plus hoặc SQL Developer

### Lỗi: Export chậm
- Thêm index trên bảng BANDONEN:
  ```sql
  CREATE INDEX idx_bandonen_zoom ON BANDONEN(ZOOM, X, Y);
  ```

### File MBTiles quá lớn
- Export theo từng zoom level
- Nén file bằng `sqlite3` vacuum command
