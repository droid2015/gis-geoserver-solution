# Installation Guide

Hướng dẫn chi tiết cài đặt GIS GeoServer Solution.

## Yêu cầu hệ thống

### Hardware
- CPU: 2+ cores (khuyến nghị 4 cores)
- RAM: 4GB minimum (khuyến nghị 8GB)
- Disk: 10GB free space (khuyến nghị 20GB)

### Software
- **Docker**: Version 20.x trở lên
- **Docker Compose**: Version 2.x trở lên
- **Git**: Để clone repository

### Operating System
- Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+)
- macOS (10.15+)
- Windows 10/11 với WSL2

## Cài đặt Docker

### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install dependencies
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker compose version
```

### macOS

1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Install và follow wizard
3. Start Docker Desktop
4. Verify:
```bash
docker --version
docker compose version
```

### Windows (WSL2)

1. Install WSL2: https://docs.microsoft.com/en-us/windows/wsl/install
2. Download Docker Desktop: https://www.docker.com/products/docker-desktop
3. Install Docker Desktop với WSL2 backend
4. Open PowerShell và verify:
```powershell
docker --version
docker compose version
```

## Cài đặt GIS GeoServer Solution

### 1. Clone Repository

```bash
git clone https://github.com/droid2015/gis-geoserver-solution.git
cd gis-geoserver-solution
```

### 2. Setup Environment

```bash
make setup
```

Hoặc manual:

```bash
cp .env.example .env
mkdir -p pgdata geoserver_data uploads
```

### 3. Configure Environment Variables

Edit file `.env`:

```bash
nano .env
```

**Important variables to change:**

```env
# Database - Change password!
POSTGRES_PASSWORD=your_secure_password_here

# GeoServer - Change password!
GEOSERVER_ADMIN_PASSWORD=your_geoserver_password_here

# Application secret key - Generate random string
SECRET_KEY=generate_a_random_secret_key_here
```

**Generate random secret key:**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Start Services

```bash
make start
```

Hoặc:

```bash
docker-compose up -d
```

**Đợi services khởi động** (1-2 phút):

```bash
# Monitor logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 5. Verify Installation

**Check all services are running:**

```bash
docker-compose ps
```

Expected output:
```
NAME                STATUS              PORTS
gis-backend         Up                  0.0.0.0:8000->8000/tcp
gis-frontend        Up                  0.0.0.0:3000->3000/tcp
gis-geoserver       Up (healthy)        0.0.0.0:8080->8080/tcp
gis-postgres        Up (healthy)        0.0.0.0:5432->5432/tcp
```

**Test endpoints:**

```bash
# Backend health
curl http://localhost:8000/api/health

# Database health
curl http://localhost:8000/api/health/database

# GeoServer health
curl http://localhost:8000/api/health/geoserver
```

### 6. Initialize GeoServer

Run initialization script:

```bash
docker-compose exec backend python scripts/geoserver-init.py
```

Expected output:
```
============================================================
GeoServer Auto-Configuration Script
============================================================
Waiting for GeoServer at http://geoserver:8080/geoserver...
✅ GeoServer is ready!
Creating workspace: gis_workspace
✅ Workspace 'gis_workspace' created successfully
Creating PostGIS datastore: postgis_store
✅ Datastore 'postgis_store' created successfully
Publishing layer: vietnam_cities
✅ Layer 'vietnam_cities' published successfully
============================================================
✅ GeoServer configuration completed successfully!
============================================================
```

### 7. Access Applications

Open trong browser:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **GeoServer**: http://localhost:8080/geoserver
  - Username: `admin`
  - Password: từ `.env` (default: `geoserver`)

## Post-Installation

### Test Upload

1. Truy cập http://localhost:3000
2. Click tab "Upload"
3. Upload file `data/vietnam_cities.geojson`
4. Layer name: `test_cities`
5. Click Upload
6. Map sẽ hiển thị data

### Test Spatial Query

1. Click tab "Query"
2. Layer name: `vietnam_cities`
3. Query type: Bounding Box
4. Click Execute Query
5. Results sẽ hiển thị trên map

## Troubleshooting

### Port conflicts

Nếu ports đã được sử dụng:

1. Edit `.env`:
```env
# Change ports
BACKEND_PORT=8001
GEOSERVER_PORT=8081
```

2. Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # backend
  - "8081:8080"  # geoserver
```

### Memory issues

Nếu services bị crash do memory:

1. Increase Docker memory limit (Docker Desktop > Settings > Resources)
2. Reduce GeoServer memory trong `.env`:
```env
INITIAL_MEMORY=1G
MAXIMUM_MEMORY=2G
```

### Database connection refused

```bash
# Check PostgreSQL logs
docker-compose logs postgres-postgis

# Restart PostgreSQL
docker-compose restart postgres-postgis

# Wait for health check
docker-compose ps
```

### GeoServer not starting

```bash
# Check logs
docker-compose logs geoserver

# Increase startup timeout
# Edit docker-compose.yml healthcheck start_period
start_period: 120s  # from 60s
```

### Frontend build errors

```bash
# Rebuild frontend
docker-compose build frontend

# Clear npm cache
docker-compose run frontend npm cache clean --force
docker-compose up -d
```

## Uninstall

### Stop services

```bash
make stop
```

### Remove all data (WARNING: Deletes everything!)

```bash
make clean
```

Or manual:

```bash
docker-compose down -v
rm -rf pgdata/ geoserver_data/ uploads/
```

### Remove Docker images

```bash
docker-compose down --rmi all
```

## Next Steps

- [User Guide](USER_GUIDE.md) - Hướng dẫn sử dụng
- [API Documentation](API.md) - API reference
- [Development Guide](DEVELOPMENT.md) - Development setup
