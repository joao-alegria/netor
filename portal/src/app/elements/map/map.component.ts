import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';

import * as L from 'leaflet';
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  map
  marker
  predefinedLocations = { "Aveiro Location": [40.6341, -8.6599], "Madrid Location": [40.3151, -3.7247], "Italy Location": [43.6800, 10.3500] }

  @Input() set coords(value: any) {
    if (this.marker != null) {
      this.map.removeLayer(this.marker)
      this.marker = L.marker(value).addTo(this.map).bindPopup("Selected Location.")
    }
  };

  @Output() onConfirm = new EventEmitter<any>();

  constructor() { }

  ngOnInit() {
    var mymap = L.map('mapid').setView([48, 15], 4);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 20,
      minZoom: 1,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1
    }).addTo(mymap);
    this.map = mymap

    var popup = L.popup();

    var _onConfirm = this.onConfirm
    var _this = this

    function onMapClick(e) {
      let additionalInfo = ""
      let coords = [parseFloat(e.latlng.lat.toFixed(4)), parseFloat(e.latlng.lng.toFixed(4))]
      for (var location in _this.predefinedLocations) {
        if (JSON.stringify(coords) == JSON.stringify(_this.predefinedLocations[location])) {
          additionalInfo = location + " "
          break
        }
      }

      popup
        .setLatLng(coords)
        .setContent('<p id="info">You clicked the map at <b>' + additionalInfo + '</b>' + JSON.stringify(coords) + '</p><button id="cancel" class="btn btn-secondary btn-sm">cancel</button><button style="float:right" class="btn btn-primary btn-sm" id="confirm">confirm</button>')
        .openOn(mymap);

      L.DomEvent.on(document.getElementById("confirm"), 'click', (e) => {
        _onConfirm.emit(coords)
        mymap.closePopup()
        if (_this.marker != null) {
          mymap.removeLayer(_this.marker)
        }
        _this.marker = L.marker(coords).addTo(mymap).bindPopup("Selected Location.")
      })

      L.DomEvent.on(document.getElementById("cancel"), 'click', () => {
        mymap.closePopup()
      })
    }

    mymap.on('click', onMapClick);


    // Icon options
    var iconOptions = {
      iconUrl: 'assets/locationMarker.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    }

    // Creating a custom icon
    var customIcon = L.icon(iconOptions);
    for (let location in this.predefinedLocations) {
      let tmpmarker = L.marker(this.predefinedLocations[location], { icon: customIcon }).addTo(this.map).bindPopup(location).on("click", onMapClick)
      tmpmarker._icon.classList.add("huechange")
    }

  }


}
