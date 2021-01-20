L.mapbox.accessToken = 'pk.eyJ1IjoicmFmdW5nIiwiYSI6ImNramdrbjBsdDN3c2Iyem5xMGJ1cTBzemIifQ.550TU0Z5yySD8mteqHIOKQ';


var mapboxTiles2 = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=' + L.mapbox.accessToken, {
       attribution: '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
       tileSize: 512,
       zoomOffset: -1,
       maxZoom: 18,
       tileSize: 512
});

var select_map = L.map('select_mapid')
     .addLayer(mapboxTiles2)
     .setView([8.2280,124.2452], 8);
var marker = L.marker(coordinates).addTo(select_map);
