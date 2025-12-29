# User Guide

Hướng dẫn sử dụng GIS GeoServer Solution cho end users.

## Giới thiệu

GIS GeoServer Solution là một web application cho phép bạn:
- Xem và tương tác với bản đồ
- Quản lý các layers (lớp dữ liệu)
- Upload dữ liệu spatial (Shapefile, GeoJSON)
- Thực hiện spatial queries
- Publish layers lên GeoServer

## Truy cập ứng dụng

Mở browser và truy cập: **http://localhost:3000**

## Giao diện chính

### Header
- **Logo/Title**: GIS GeoServer Solution
- **API Docs**: Link đến API documentation
- **GeoServer**: Link đến GeoServer admin

### Sidebar (bên trái)
- **Layers**: Quản lý layers
- **Upload**: Upload dữ liệu
- **Query**: Spatial queries

### Map Area (bên phải)
- Interactive map với OpenLayers
- Base map: OpenStreetMap
- Controls: Zoom, Full Screen, Scale Line
- Mouse Position: Hiển thị tọa độ

## Layers Tab

### View Layers

1. Click tab **Layers**
2. Danh sách layers hiển thị
3. Mỗi layer có:
   - Checkbox: Toggle visibility
   - Name/Title
   - Opacity slider
   - Actions buttons

### Toggle Visibility

1. Click checkbox bên cạnh layer name
2. Layer sẽ hiện/ẩn trên map

### Adjust Opacity

1. Kéo opacity slider
2. Layer transparency thay đổi (0% = trong suốt, 100% = không trong suốt)

### Publish to GeoServer

1. Click button **Publish** trên layer
2. Layer sẽ được publish lên GeoServer
3. Có thể truy cập qua WMS/WFS services

### Delete Layer

1. Click button **Delete**
2. Confirm deletion
3. Layer và data sẽ bị xóa

## Upload Tab

### Upload GeoJSON

1. Click tab **Upload**
2. Drag & drop file `.geojson` vào drop zone
   - Hoặc click để browse file
3. Enter layer name (auto-generate từ filename)
4. Click **Upload**
5. Đợi upload complete
6. Layer mới xuất hiện trong Layers tab

### Upload Shapefile

1. Click tab **Upload**
2. Prepare shapefile:
   - ZIP file containing: .shp, .shx, .dbf, .prj
3. Drag & drop ZIP file vào drop zone
4. Enter layer name
5. Click **Upload**
6. System sẽ import vào PostGIS
7. Layer mới available trong Layers tab

**Shapefile requirements:**
- Must be in ZIP format
- Must contain: .shp, .shx, .dbf
- Should contain: .prj (projection)

## Query Tab

### Bounding Box Query

1. Click tab **Query**
2. Enter layer name (e.g., `vietnam_cities`)
3. Select query type: **Bounding Box**
4. Enter coordinates:
   - Min X (longitude): 105.0
   - Min Y (latitude): 10.0
   - Max X: 109.0
   - Max Y: 22.0
5. Click **Execute Query**
6. Results hiển thị trên map
7. Feature count hiển thị trong toast notification

### Other Query Types

**Intersect**: Find features intersecting với một geometry
**Buffer**: Find features trong buffer distance
**Within**: Find features within a polygon

## Map Interactions

### Zoom
- Mouse wheel: Scroll để zoom in/out
- Zoom controls: Click +/- buttons
- Double click: Zoom in

### Pan
- Click and drag: Di chuyển map

### Feature Info
- Click vào feature trên map
- Popup hiển thị feature properties:
  - Name
  - Population
  - Type
  - etc.

### Full Screen
- Click Full Screen button (top right)
- Press Esc để exit

### Mouse Position
- Di chuyển mouse trên map
- Tọa độ hiển thị bottom right (latitude, longitude)

## Best Practices

### Layer Management
- Tên layers nên descriptive và unique
- Use lowercase và underscores (e.g., `vietnam_cities`)
- Delete unused layers để tiết kiệm storage

### Data Upload
- Check coordinate system (EPSG:4326 recommended)
- Validate data trước khi upload
- Keep file sizes reasonable (<50MB)

### Queries
- Start with small bounding boxes
- Test queries trước khi expand
- Check feature count để avoid overload

## Common Tasks

### Visualize Sample Data

1. Truy cập http://localhost:3000
2. Tab Layers
3. Vietnam Cities layer đã có sẵn
4. Toggle visibility để xem
5. Zoom to Vietnam region
6. Click cities để xem info

### Add New City Data

1. Prepare GeoJSON file với cities
2. Upload tab
3. Upload file
4. Layer name: `new_cities`
5. View trên map
6. Query để verify data

### Compare Two Layers

1. Upload hai layers
2. Layers tab
3. Enable both layers
4. Adjust opacity to see both
5. Use different queries để analyze

## Troubleshooting

### Map không load
- Check internet connection (base map needs internet)
- Refresh page
- Check browser console for errors

### Upload fails
- Verify file format (.zip cho shapefile, .geojson cho GeoJSON)
- Check file size (<100MB)
- Ensure valid spatial data

### Query returns no results
- Check layer name spelling
- Verify bounding box coordinates
- Ensure features exist in that area

### Layer không hiển thị
- Check visibility checkbox
- Adjust opacity
- Zoom to appropriate level

## Support

Nếu gặp vấn đề:
1. Check [Installation Guide](INSTALLATION.md)
2. Review [API Documentation](API.md)
3. Check logs: `docker-compose logs`
4. Open GitHub issue
