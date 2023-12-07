class NcMap {
  constructor() {
      this.map = null;
  }

  fetch_data_and_render_map(){
    const self = this;
    $.ajax({
      type: 'GET',
      url: 'http://localhost:5000/fetch_geojson', // have to change to the server URL once hosted (don't forget HTTPS)
    }).done(( response ) => {
       const data = JSON.parse(response).data;
       self.render_map(data);
       const status = '*Note: Sections of the roadway marked as "<span style="color:lightgreen">ungated</span>" are open except in emergency situations.' +
          '<br/>' + 'Last Updated: ' + data.metadata.last_update +
          '<br/>' + 'Source: <a href="https://www.nps.gov/blri/planyourvisit/roadclosures.htm">https://www.nps.gov/blri/planyourvisit/roadclosures.htm</a>'
       $('#status').html(status);
    });
  }

  render_map(data){
    const map_center = [data.metadata.map_center.lat, data.metadata.map_center.long]
    this.map = L.map('nc_map').setView(map_center, 10);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: '',  // populate with API key
    }).addTo(this.map);
    this.render_routes(data.features);

    // add dynamic line thickness by zoom level
    this.map.on('zoomend', () => {
        const current_zoom = this.map.getZoom();
        const base_weight = current_zoom > 10 ? (current_zoom / 1.5) : 3;  //arbitrary values based on my eyeballs
        this.map.eachLayer( (layer) => {
            if (layer instanceof L.Path) { // only manipulate Path objects
                // if it's a point, it needs to be biggererer
                const weight = Object.keys(layer.options).includes('radius') ? base_weight * 3 : base_weight;
                layer.setStyle({weight});
            }
        });
    });
  }

  render_routes(features){
    const geojson_marker_options = {
      radius: 3,
      fillColor: '#fff',
      color: '#000',
      weight: 9,
      opacity: 0.8,
      fillOpacity: 0.1
    };

    const geojson_features = L.geoJSON(features, {
      style: (feature) => {
          switch (feature.properties.status) {
              case 'Closed': return {color: 'red'};
              case 'Open':   return {color: 'green'};
              case 'Ungated*': return {color: 'lightgreen'};
              // will default to blue if different status
          }
      },
      pointToLayer: (feature, latlng) => {
          return L.circleMarker(latlng, geojson_marker_options);
      },
      onEachFeature: (feature, layer) => {
          const original_color = layer.options.color
          let info = '<h3>' + feature.properties.name + '</h3>';
          info += '<div>Milepost ' + feature.properties.parkway_mileposts + '</div>';
          info += '<div><i>' + feature.properties.description + '</i></div>';
          info += feature.properties.notes ? ('<div>Notes: ' + feature.properties.notes + '</div>') : '';
          info += '<div><b>' + feature.properties.status + '</b></div>';
          layer.bindPopup(info);
          layer.on('mouseover', (e) => layer.setStyle({color: 'magenta'}));
          layer.on('mouseout', (e) => layer.setStyle({color: original_color}));
      }
    });
    geojson_features.addTo(this.map);
  }
}

const nc_map = new NcMap()
nc_map.fetch_data_and_render_map()
