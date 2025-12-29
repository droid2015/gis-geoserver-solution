# Giải Pháp GIS với GeoServer

Giải pháp GIS mã nguồn mở hoàn chỉnh sử dụng GeoServer, PostgreSQL+PostGIS, FastAPI và React+OpenLayers.

## ✨ Tính năng

- 🗺️ Interactive web map với OpenLayers 8
- 📊 Quản lý layers và spatial data
- ⬆️ Upload Shapefile và GeoJSON
- 🔍 Spatial queries và analysis (bbox, intersect, buffer, within)
- 🌐 WMS/WFS services từ GeoServer
- 🐳 Docker Compose deployment
- 📍 Sample data: Các thành phố Việt Nam

## 🏗️ Kiến trúc

```
┌──────────────────────────────────┐
│     React + OpenLayers           │
│     (Frontend Web Client)        │
│     Port: 3000                   │
└────────────┬─────────────────────┘
             │
             ├──────────────┬──────────────────┐
             │              │                  │
┌────────────▼─────┐ ┌─────▼──────────┐      │
│   FastAPI        │ │   GeoServer    │      │
│   Backend API    │ │   Map Server   │      │
│   Port: 8000     │ │   Port: 8080   │      │
└────────────┬─────┘ └────────┬───────┘      │
             │                │               │
             └────────┬───────┘               │
                      │                       │
            ┌─────────▼──────────────┐        │
            │  PostgreSQL + PostGIS  │        │
            │  Spatial Database      │        │
            │  Port: 5432            │        │
            └────────────────────────┘        │
```

**Tech Stack:**
- **Frontend**: React 18 + OpenLayers 8
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15 + PostGIS 3.4
- **Map Server**: GeoServer 2.24
- **Deployment**: Docker Compose

## 🚀 Quick Start

### Yêu cầu

- Docker 20.x+
- Docker Compose 2.x+
- 4GB RAM (khuyến nghị 8GB)
- 10GB disk space

### Cài đặt

1. **Clone repository:**
```bash
git clone https://github.com/droid2015/gis-geoserver-solution.git
cd gis-geoserver-solution
```

2. **Setup environment:**
```bash
make setup
```
Lệnh này sẽ:
- Copy `.env.example` thành `.env`
- Tạo các thư mục cần thiết (pgdata, geoserver_data, uploads)

3. **Chỉnh sửa `.env`** (nếu cần):
```bash
nano .env
```
Thay đổi passwords, ports nếu cần.

4. **Start services:**
```bash
make start
```
Đợi 1-2 phút để các services khởi động.

5. **Truy cập ứng dụng:**
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **GeoServer**: http://localhost:8080/geoserver (admin/geoserver)

### First Time Setup

Sau khi services đã chạy, cấu hình GeoServer:

```bash
docker-compose exec backend python scripts/geoserver-init.py
```

Script này sẽ tự động:
- Tạo workspace `gis_workspace`
- Tạo PostGIS datastore `postgis_store`
- Publish layer mẫu `vietnam_cities`

## 📖 Documentation

Chi tiết documentation:
- [Installation Guide](docs/INSTALLATION.md) - Hướng dẫn cài đặt chi tiết
- [API Documentation](docs/API.md) - API endpoints và usage
- [User Guide](docs/USER_GUIDE.md) - Hướng dẫn sử dụng
- [Development Guide](docs/DEVELOPMENT.md) - Development setup

## 🛠️ Makefile Commands

```bash
make help       # Hiển thị help
make setup      # Initial setup
make start      # Start tất cả services
make stop       # Stop tất cả services
make restart    # Restart services
make logs       # Xem logs (tail -f)
make clean      # Dọn dẹp volumes (xóa data!)
make test       # Run backend tests
```

## 📁 Cấu trúc Project

```
gis-geoserver-solution/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── utils/       # Utilities
│   ├── package.json
│   └── Dockerfile
├── database/             # Database init scripts
│   └── init.sql
├── scripts/              # Utility scripts
│   └── geoserver-init.py
├── styles/               # GeoServer SLD styles
│   ├── point_style.sld
│   └── polygon_style.sld
├── data/                 # Sample data
│   └── vietnam_cities.geojson
├── docs/                 # Documentation
├── docker-compose.yml    # Docker Compose config
├── Makefile             # Helper commands
├── .env.example         # Environment template
└── README.md            # This file
```

## 🎯 Features Detail

### Layer Management
- Create, read, update, delete layers
- Toggle visibility
- Adjust opacity
- Layer metadata

### Data Upload
- Drag & drop interface
- Shapefile upload (.zip)
- GeoJSON upload (.geojson, .json)
- Automatic import to PostGIS

### Spatial Queries
- Bounding box query
- Intersection query
- Buffer analysis
- Within (point in polygon)

### Map Features
- OpenLayers interactive map
- OSM base map
- Vector rendering
- Feature info on click
- Mouse position display
- Scale line
- Full screen mode

### GeoServer Integration
- Automatic workspace creation
- PostGIS datastore configuration
- Layer publishing
- WMS/WFS services

## 🔧 Configuration

### Environment Variables

Xem file `.env.example` để biết tất cả configuration options.

**Key variables:**
- `POSTGRES_PASSWORD` - Database password
- `GEOSERVER_ADMIN_PASSWORD` - GeoServer admin password
- `CORS_ORIGINS` - Allowed CORS origins

### Ports

Default ports:
- Frontend: 3000
- Backend: 8000
- GeoServer: 8080
- PostgreSQL: 5432

Thay đổi trong `.env` hoặc `docker-compose.yml` nếu cần.

## 🐛 Troubleshooting

### Services không start

```bash
# Check logs
make logs

# Check individual service
docker-compose logs backend
docker-compose logs geoserver
docker-compose logs postgres-postgis
```

### GeoServer không connect được

1. Đảm bảo GeoServer đã start hoàn toàn (có thể mất 60-90s)
2. Check logs: `docker-compose logs geoserver`
3. Thử truy cập: http://localhost:8080/geoserver

### Database connection errors

1. Check PostgreSQL logs: `docker-compose logs postgres-postgis`
2. Verify credentials trong `.env`
3. Đảm bảo port 5432 không bị chiếm dụng

### Frontend không load

1. Check backend API: http://localhost:8000/api/health
2. Check browser console for errors
3. Verify CORS settings trong `.env`

## 📝 API Endpoints

### Health Checks
- `GET /api/health` - API status
- `GET /api/health/database` - Database connection
- `GET /api/health/geoserver` - GeoServer connection

### Layers
- `GET /api/layers` - List layers
- `POST /api/layers` - Create layer
- `PUT /api/layers/{id}` - Update layer
- `DELETE /api/layers/{id}` - Delete layer

### Upload
- `POST /api/upload/shapefile` - Upload shapefile
- `POST /api/upload/geojson` - Upload GeoJSON

### Query
- `POST /api/query/bbox` - Bounding box query
- `POST /api/query/intersect` - Intersection query
- `POST /api/query/buffer` - Buffer query
- `POST /api/query/within` - Within query

Xem full documentation tại: http://localhost:8000/docs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 👤 Author

**droid2015**
- GitHub: [@droid2015](https://github.com/droid2015)

## 🙏 Acknowledgments

- GeoServer
- PostGIS
- FastAPI
- React
- OpenLayers

---

**Happy Mapping! 🗺️** 
