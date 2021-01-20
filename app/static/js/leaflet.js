var locations = [
       ["LOCATION_1", 11.8166, 122.0942],
       ["LOCATION_2", 11.9804, 121.9189],
       ["LOCATION_3", 10.7202, 122.5621],
       ["LOCATION_4", 11.3889, 122.6277],
       ["LOCATION_5", 10.5929, 122.6325]
     ];
     

L.mapbox.accessToken = 'pk.eyJ1IjoicmFmdW5nIiwiYSI6ImNramdrbjBsdDN3c2Iyem5xMGJ1cTBzemIifQ.550TU0Z5yySD8mteqHIOKQ';
    
var mapboxTiles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=' + L.mapbox.accessToken, {
       attribution: '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
       tileSize: 512,
       zoomOffset: -1,
       maxZoom: 18,
       tileSize: 512
});

var map = L.map('mapid')
  .addLayer(mapboxTiles)
  .setView([11.206051, 122.447886], 8);

  for (var i = 0; i < locations.length; i++) {
       marker = new L.marker([locations[i][1], locations[i][2]])
         .bindPopup(locations[i][0])
         .addTo(map);
     }