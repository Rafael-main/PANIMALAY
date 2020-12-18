
var data = JSON.parse('{{ data | tojson | safe}}');
console.log(data)

mapboxgl.accessToken = 'pk.eyJ1IjoicmFmdW5nIiwiYSI6ImNrZnBkdDIzZDA2b3IzMnBnajA4dWFyemIifQ.cEp_Rxe4yleIAIcd9CLb3g';
var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/rafung/cki4no1nr39c519pqjpbyng2q',
  center: [-74.5, 40], // starting position [lng, lat]
  zoom: 9 // starting zoom        
});
var marker = new mapboxgl.Marker()
.setLngLat([124.4, 8.25])
.addTo(map);