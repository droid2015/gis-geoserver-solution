# Sample Data

## Vietnam Cities

File: `vietnam_cities.geojson`

### Description

Sample GeoJSON data containing 10 major cities in Vietnam with their locations and basic information.

### Attributes

- `name` (Vietnamese): City name in Vietnamese
- `name_en` (English): City name in English
- `population` (Integer): Estimated population
- `type` (String): City type (Capital, City, Province Capital)
- `description` (String): Brief description

### Cities Included

1. **Hà Nội (Hanoi)** - Capital, Population: 8,000,000
2. **TP Hồ Chí Minh (Ho Chi Minh City)** - Largest city, Population: 9,000,000
3. **Đà Nẵng (Da Nang)** - Central coast, Population: 1,200,000
4. **Hải Phòng (Hai Phong)** - Northern port, Population: 2,000,000
5. **Cần Thơ (Can Tho)** - Mekong Delta, Population: 1,200,000
6. **Huế (Hue)** - Ancient imperial capital, Population: 340,000
7. **Nha Trang** - Coastal resort, Population: 400,000
8. **Vũng Tàu (Vung Tau)** - Southern coast, Population: 450,000
9. **Quy Nhơn (Quy Nhon)** - Central coast, Population: 280,000
10. **Buôn Ma Thuột (Buon Ma Thuot)** - Central Highlands, Population: 340,000

### Coordinate System

- EPSG:4326 (WGS 84)
- Longitude, Latitude format

### Usage

This sample data is automatically loaded into the PostgreSQL+PostGIS database during initialization and is available for testing the GIS system.

### Data Sources

Population data is approximate and for demonstration purposes only.

## Highways Data

### TP.HCM - Trung Lương Expressway

- **Name**: Cao tốc TP Hồ Chí Minh - Trung Lương
- **English Name**: Ho Chi Minh City - Trung Luong Expressway
- **Type**: Expressway
- **Length**: 62 km
- **Lanes**: 4 lanes
- **Max Speed**: 120 km/h
- **Status**: Operational
- **Opened**: July 31, 2010
- **Description**: First expressway in Vietnam, connecting Ho Chi Minh City with Mekong Delta region

**Coordinates**: LineString from HCMC (106.6297, 10.8231) to Trung Luong (106.7650, 10.4500)

**Source**: OpenStreetMap, Vietnam Expressway Corporation
