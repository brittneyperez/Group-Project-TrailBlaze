(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
({key: "AIzaSyC3wzK_IRzTkYzszfImdCmdYeU02Mbwr4A", v: "weekly"});

function get_user_loc(){
    return userlat, userlong;
}
let map, infoWindow;

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


  map.addListener("click", (event) => {
    closeInfoWindow(); 
    openInfoWindow(event.latLng); 
  });
}

function openInfoWindow(location) {
  if (!infoWindow) {
    infoWindow = new google.maps.InfoWindow({
      content: getInfoWindowContent(location),
    });

    infoWindow.addListener("closeclick", () => {
      infoWindow = null; 
    });

    infoWindow.setPosition(location); 
    infoWindow.open(map); 
  }
}

function getInfoWindowContent(location) {
  return `
    <div>
      <p>Do you want to add a marker at this location?</p>
      <button onclick="addMarker(${location.lat()}, ${location.lng()})">Add Marker</button>
      <button onclick="closeInfoWindow()">Cancel</button>
    </div>
  `;
}

function addMarker(lat, lng) {
  new google.maps.Marker({
    position: { lat, lng },
    map: map,
    title: "Custom Marker",
  });
  closeInfoWindow();
}

function closeInfoWindow() {
  if (infoWindow) {
    infoWindow.close();
    infoWindow = null;
  }
}

google.maps.importLibrary("geometry", "drawing").then(() => {
  initMap();
});
