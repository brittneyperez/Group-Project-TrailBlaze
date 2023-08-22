(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
({key: "AIzaSyC3wzK_IRzTkYzszfImdCmdYeU02Mbwr4A", v: "weekly"});

function get_user_loc(){
    return userlat, userlong;
}
let map, infoWindow;
let markers = [];
let markerListElement;
let autocomplete;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: userlat, lng: userlong },
    zoom: 8,
  });

  new google.maps.Marker({
    position: { lat: userlat, lng: userlong },
    map: map,
    title: "Your Location",
  });

  markerListElement = document.getElementById("markerList");

  google.maps.importLibrary("places").then(() => {
    const locationInput = document.getElementById("locationInput");
    autocomplete = new google.maps.places.Autocomplete(locationInput);

    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();
      if (!place.geometry) {
        return;
      }
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    });

    locationInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        performAutocompleteSearch(locationInput.value);
      }
  });
  });


  map.addListener("click", (event) => {
    closeInfoWindow(); 
    openInfoWindow(event.latLng); 
  });
}
function performAutocompleteSearch(query) {
  if (autocomplete && query.trim() !== "") {
    const autocompleteService = new google.maps.places.AutocompleteService();
    autocompleteService.getPlacePredictions({ input: query }, (predictions, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK && predictions && predictions.length > 0) {
        const placeService = new google.maps.places.PlacesService(map);
        placeService.getDetails({ placeId: predictions[0].place_id }, (result, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK && result.geometry) {
            map.setCenter(result.geometry.location);
            map.setZoom(14);

            const confirmButton = document.querySelector("#infoWindowConfirmButton");
            if (confirmButton) {
              confirmButton.click();
            }
          }
        });
      }
    });
  }
}

function getInfoWindowContent(location) {
  return `
    <div>
      <p>Do you want to add a marker at this location?</p>
      <p>Address: <span id="address"></span></p>
      <button id="infoWindowConfirmButton" onclick="confirmAddMarker(${location.lat()}, ${location.lng()},  document.getElementById('address').textContent)">Add Marker</button>
      <button onclick="closeInfoWindow()">Cancel</button>
    </div>
  `;
}

function get_address_from_latlng(lat, lng, callback) {
  var geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(lat, lng);
  
  geocoder.geocode({ 'latLng': latlng }, function (results, status) {
    if (status !== google.maps.GeocoderStatus.OK) {
      alert(status);
      callback(null); // Pass null if an error occurred
    }
    if (status == google.maps.GeocoderStatus.OK) {
      var address = (results[0].formatted_address);
      console.log(address);
      callback(address); // Pass the address to the callback
    }
  });
}

async function openInfoWindow(location) {
  infoWindow = new google.maps.InfoWindow({
    content: getInfoWindowContent(location),
  });

  infoWindow.addListener("closeclick", () => {
    closeInfoWindow();
  });

  infoWindow.setPosition(location); // Set the position of the info window
  infoWindow.open(map); // Open the info window



  // Retrieve and set the address in the info window
  get_address_from_latlng(location.lat(), location.lng(), (address) => {
    const addressElement = document.getElementById("address");
    if (addressElement && address) {
      addressElement.textContent = address;
      
    }
  });
}
function confirmAddMarker(lat,lng, address) {
  addMarker(lat,lng, address);
  closeInfoWindow();
  updateMarkerList(lat, lng, address);
}

function addMarker(lat, lng, title) {
  const marker = new google.maps.Marker({
    position: { lat, lng },
    lat: lat,
    lng: lng,
    map: map,
    title: title,
  });
  markers.push(marker);
}

function updateMarkerList() {
  if (markerListElement) {
    markerListElement.innerHTML = markers
    .map((marker, index) => `<p>Marker ${index + 1}: ${marker.title}: ${marker.lat.toFixed(2)},  ${marker.lng.toFixed(2)}</p>`)
    .join("");
    console.log(markerListElement.innerHTML);
    console.log(markers);
}
}
function closeInfoWindow() {
  if (infoWindow) {
    infoWindow.close();
    infoWindow = null;
  }
}

function clearMarkers() { 
  markers.forEach((marker) => marker.setMap(null));
  markers = [];
  updateMarkerList();
}


// bind the clearMarkers and deleteMarkers functions to the buttons
document.getElementById("clearMarkers").addEventListener("click", clearMarkers);

google.maps.importLibrary("geometry", "drawing").then(() => {
  initMap();
});
