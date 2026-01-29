@echo off
REM Script tạo layer Oracle Basemap trong GeoServer (Windows)

set GEOSERVER_URL=http://localhost:8080/geoserver
set GEOSERVER_USER=admin
set GEOSERVER_PASS=geoserver
set WORKSPACE=basemap
set STORE_NAME=oracle_tiles
set LAYER_NAME=oracle_basemap

echo ===================================================
echo Setup Oracle Basemap Layer in GeoServer
echo ===================================================
echo.

REM 1. Tạo workspace
echo Step 1: Creating workspace...
docker exec gis-geoserver curl -u %GEOSERVER_USER%:%GEOSERVER_PASS% -X POST ^
  "%GEOSERVER_URL%/rest/workspaces" ^
  -H "Content-Type: application/json" ^
  -d "{\"workspace\":{\"name\":\"%WORKSPACE%\"}}"

echo.

REM 2. Tạo Coverage Store (ImageMosaic)
echo Step 2: Creating Coverage Store...
docker exec gis-geoserver curl -u %GEOSERVER_USER%:%GEOSERVER_PASS% -X PUT ^
  "%GEOSERVER_URL%/rest/workspaces/%WORKSPACE%/coveragestores/%STORE_NAME%/external.imagemosaic" ^
  -H "Content-Type: text/plain" ^
  -d "file:///opt/geoserver/data_dir/tiles/oracle_basemap"

echo.

REM 3. Publish layer từ store
echo Step 3: Publishing layer...
docker exec gis-geoserver curl -u %GEOSERVER_USER%:%GEOSERVER_PASS% -X POST ^
  "%GEOSERVER_URL%/rest/workspaces/%WORKSPACE%/coveragestores/%STORE_NAME%/coverages" ^
  -H "Content-Type: application/json" ^
  -d "{\"coverage\":{\"name\":\"%LAYER_NAME%\",\"title\":\"Oracle Basemap\",\"enabled\":true}}"

echo.

REM 4. Enable tile caching
echo Step 4: Enabling tile caching...
docker exec gis-geoserver curl -u %GEOSERVER_USER%:%GEOSERVER_PASS% -X PUT ^
  "%GEOSERVER_URL%/gwc/rest/layers/%WORKSPACE%:%LAYER_NAME%.xml" ^
  -H "Content-Type: application/xml" ^
  -d "<GeoServerLayer><name>%WORKSPACE%:%LAYER_NAME%</name><enabled>true</enabled><mimeFormats><string>image/png</string></mimeFormats><gridSubsets><gridSubset><gridSetName>EPSG:3857</gridSetName></gridSubset></gridSubsets></GeoServerLayer>"

echo.
echo ===================================================
echo Setup completed!
echo ===================================================
echo.
echo Layer details:
echo - Workspace: %WORKSPACE%
echo - Layer: %WORKSPACE%:%LAYER_NAME%
echo - WMS URL: %GEOSERVER_URL%/wms
echo - WMTS URL: %GEOSERVER_URL%/gwc/service/wmts
echo.
echo Test in browser:
echo %GEOSERVER_URL%/web
echo.
pause
