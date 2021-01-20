var mymap = L.map('mapid').setView([51.505, -0.09], 13);


L.tileLayer('https://api.mapbox.com/styles/v1/rafung/ckjgknq8w6zzl1aqsxexel2ec.html?fresh=true&title=view&access_token=pk.eyJ1IjoicmFmdW5nIiwiYSI6ImNrZnBkdDIzZDA2b3IzMnBnajA4dWFyemIifQ.cEp_Rxe4yleIAIcd9CLb3g', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoicmFmdW5nIiwiYSI6ImNramdrbjBsdDN3c2Iyem5xMGJ1cTBzemIifQ.550TU0Z5yySD8mteqHIOKQ'
}).addTo(mymap);


