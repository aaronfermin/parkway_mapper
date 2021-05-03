class NcMap {
  constructor() {
      this.data = null;
      this.map = null;
  }

  fetch_data_and_render_map(){
    const self = this;
    $.ajax({
      type: "GET",
      url: "http://localhost:5000/nc_geojson",
    }).done(function( response ) {
       self.data = JSON.parse(response).data;
       self.render_map();
       const status = '*Note: Sections of the roadway marked as "ungated" are open except in emergency situations.' +
          '<br/>' + 'Last Updated: ' + self.data.metadata.last_update +
          '<br/>' + 'Last Requested: ' + self.data.metadata.last_request
       $('#status').html(status);
    });
  }

  render_map(){
    const data = this.data;
    const map_center = [data.metadata.map_center.lat, data.metadata.map_center.long]
    this.map = L.map('nc_map').setView(map_center, 10);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiYWxtaW8iLCJhIjoiY2tvN3ZoYTh4MWJsbDJvb24yc2Fjb3NtbSJ9.QvMoJHlwi5-r6FmgMPLQgA'
    }).addTo(this.map);
    this.render_routes(data.features);
  }

  render_routes(features){
    var geojsonMarkerOptions = {
      radius: 3,
      fillColor: "#fff",
      color: "#000",
      weight: 10,
      opacity: 0.8,
      fillOpacity: 0.1
    };

    let geojson_features = L.geoJSON(features, {
      style: function(feature) {
          switch (feature.properties.status) {
              case 'Closed': return {color: "red"};
              case 'Open':   return {color: "green"};
              case 'Ungated*': return {color: "green"};
          }
      },
      pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, geojsonMarkerOptions);
      },
      onEachFeature: function (feature, layer) {
          let info = '<h3>' + feature.properties.name + '</h3>';
          info += '<div><i>' + feature.properties.description + '</i></div>';
          info += '<div><i>' + feature.properties.parkway_mileposts + '</i></div>';
          info += '<div>Notes: ' + (feature.properties.notes ? feature.properties.notes : 'None') + '</div>';
          info += '<div><b>' + feature.properties.status + '</b></div>';
          layer.bindPopup(info);
      }
    });
    geojson_features.addTo(this.map);
  }
}

let nc_map = new NcMap()
nc_map.fetch_data_and_render_map()
