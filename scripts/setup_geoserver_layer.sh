#!/bin/bash
# Script tạo layer Oracle Basemap trong GeoServer

GEOSERVER_URL="http://localhost:8080/geoserver"
GEOSERVER_USER="admin"
GEOSERVER_PASS="geoserver"
WORKSPACE="basemap"
STORE_NAME="oracle_tiles"
LAYER_NAME="oracle_basemap"

echo "==================================================="
echo "Setup Oracle Basemap Layer in GeoServer"
echo "==================================================="

# 1. Tạo workspace
echo "Step 1: Creating workspace..."
curl -u ${GEOSERVER_USER}:${GEOSERVER_PASS} -X POST \
  "${GEOSERVER_URL}/rest/workspaces" \
  -H "Content-Type: application/json" \
  -d "{\"workspace\":{\"name\":\"${WORKSPACE}\"}}"

echo ""

# 2. Tạo ImageMosaic store
echo "Step 2: Creating ImageMosaic store..."
curl -u ${GEOSERVER_USER}:${GEOSERVER_PASS} -X POST \
  "${GEOSERVER_URL}/rest/workspaces/${WORKSPACE}/coveragestores" \
  -H "Content-Type: application/json" \
  -d "{
    \"coverageStore\": {
      \"name\": \"${STORE_NAME}\",
      \"type\": \"ImageMosaic\",
      \"enabled\": true,
      \"workspace\": {
        \"name\": \"${WORKSPACE}\"
      },
      \"url\": \"file:///opt/geoserver/data_dir/tiles/oracle_basemap\"
    }
  }"

echo ""

# 3. Configure GridSet cho tile cache
echo "Step 3: Configuring GridSet..."
curl -u ${GEOSERVER_USER}:${GEOSERVER_PASS} -X PUT \
  "${GEOSERVER_URL}/gwc/rest/gridsets/ORACLE_3857.xml" \
  -H "Content-Type: application/xml" \
  -d '<gridSet>
    <name>ORACLE_3857</name>
    <srs>
      <number>3857</number>
    </srs>
    <extent>
      <coords>
        <double>-20037508.34</double>
        <double>-20037508.34</double>
        <double>20037508.34</double>
        <double>20037508.34</double>
      </coords>
    </extent>
    <scaleDenominators>
      <double>559082264.0287178</double>
      <double>279541132.0143589</double>
      <double>139770566.0071794</double>
      <double>69885283.00358972</double>
      <double>34942641.50179486</double>
      <double>17471320.75089743</double>
      <double>8735660.375448715</double>
      <double>4367830.187724357</double>
      <double>2183915.093862179</double>
      <double>1091957.546931089</double>
      <double>545978.7734655447</double>
      <double>272989.3867327723</double>
      <double>136494.6933663862</double>
      <double>68247.34668319309</double>
      <double>34123.67334159654</double>
      <double>17061.83667079827</double>
      <double>8530.918335399136</double>
      <double>4265.459167699568</double>
      <double>2132.729583849784</double>
    </scaleDenominators>
    <metersPerUnit>1.0</metersPerUnit>
    <pixelSize>0.00028</pixelSize>
    <tileHeight>256</tileHeight>
    <tileWidth>256</tileWidth>
  </gridSet>'

echo ""

# 4. Configure Tile Layer
echo "Step 4: Configuring Tile Layer..."
curl -u ${GEOSERVER_USER}:${GEOSERVER_PASS} -X PUT \
  "${GEOSERVER_URL}/gwc/rest/layers/${WORKSPACE}:${LAYER_NAME}.xml" \
  -H "Content-Type: application/xml" \
  -d "<GeoServerLayer>
    <name>${WORKSPACE}:${LAYER_NAME}</name>
    <enabled>true</enabled>
    <mimeFormats>
      <string>image/png</string>
      <string>image/jpeg</string>
    </mimeFormats>
    <gridSubsets>
      <gridSubset>
        <gridSetName>ORACLE_3857</gridSetName>
      </gridSubset>
    </gridSubsets>
    <metaWidthHeight>
      <int>4</int>
      <int>4</int>
    </metaWidthHeight>
    <expireCache>0</expireCache>
    <expireClients>0</expireClients>
    <parameterFilters>
      <styleParameterFilter>
        <key>STYLES</key>
        <defaultValue/>
      </styleParameterFilter>
    </parameterFilters>
  </GeoServerLayer>"

echo ""
echo "==================================================="
echo "Setup completed!"
echo "==================================================="
echo ""
echo "Layer details:"
echo "- Workspace: ${WORKSPACE}"
echo "- Layer: ${WORKSPACE}:${LAYER_NAME}"
echo "- WMS URL: ${GEOSERVER_URL}/wms"
echo "- WMTS URL: ${GEOSERVER_URL}/gwc/service/wmts"
echo ""
echo "Test URLs:"
echo "- Layer preview: ${GEOSERVER_URL}/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage"
echo "- GetCapabilities: ${GEOSERVER_URL}/wms?service=WMS&version=1.3.0&request=GetCapabilities"
echo ""
