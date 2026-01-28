@echo off
echo ==========================================
echo Export Oracle Tiles to MBTiles
echo ==========================================
echo.
echo Step 1: Update configuration in .env.oracle
echo Step 2: Run export script
echo.

REM Check if .env.oracle exists
if not exist .env.oracle (
    echo ERROR: .env.oracle file not found!
    echo Please create .env.oracle with your Oracle connection details
    pause
    exit /b 1
)

echo Starting export to MBTiles format...
python export_oracle_tiles.py mbtiles

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo Export completed successfully!
    echo ==========================================
    echo.
    echo MBTiles file: tiles_output\basemap.mbtiles
    echo.
    echo Next steps:
    echo 1. Copy basemap.mbtiles to: geoserver_data\tiles\
    echo 2. Install MBTiles plugin in GeoServer
    echo 3. Configure MBTiles store in GeoServer
    echo.
) else (
    echo.
    echo ERROR: Export failed!
    echo Please check your Oracle connection settings
    echo.
)

pause
