
var map;
var marker;
var infoWindow;
var markers = [];

var otherIcon = {
        path: google.maps.SymbolPath.CIRCLE ,
        strokeColor: "#a91245",
        fillColor: "#BC154D",
        fillOpacity: 1,
        scale: 6
    };

var defaultIcon = {
        path: google.maps.SymbolPath.CIRCLE ,
        strokeColor: "#5e2c45",
        fillColor: "#69314D",
        fillOpacity: 1,
        scale: 5
    };

var bounds = new google.maps.LatLngBounds();

function addMarker(latlng, name, icon=defaultIcon) {
  marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: name,
        icon : icon
      });
  return marker;
}

function bindInfoWindow(marker, map, infoWindow, contentString) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(contentString);
        infoWindow.open(map, marker);
        scheduleEventListenerForUber();
    });
}

function initMap() {

  var places = $('.restaurant-listing > li');
  // using ternary operator to create default lat/long when there are no restaurants in a list initially/if no lat or long exists
  var centerLatLng = { lat: ($(places[0]).data('lat') ? $(places[0]).data('lat') : 41.850033), lng: ($(places[0]).data('lng') ? $(places[0]).data('lng') : -87.6500523)};
  // SET BOUNDS DEFAULT

  var styles = [{"featureType":"administrative",
                 "elementType":"geometry.stroke",
                 "stylers":[
                    {"visibility":"on"},
                    {"color":"#0096aa"},
                    {"weight":"0.30"},
                    {"saturation":"-75"},
                    {"lightness":"5"},
                    {"gamma":"1"}]},
                {"featureType":"administrative",
                 "elementType":"labels.text.fill",
                 "stylers":[
                    {"color":"#0096aa"},
                    {"saturation":"-75"},
                    {"lightness":"5"}]},
                {"featureType":"administrative",
                 "elementType":"labels.text.stroke",
                 "stylers":[
                    {"color":"#ffc04c"},
                    {"visibility":"on"},
                    {"weight":"6"},
                    {"saturation":"-28"},
                    {"lightness":"0"}]},
                {"featureType":"administrative",
                 "elementType":"labels.icon",
                 "stylers":[
                    {"visibility":"on"},
                    {"color":"#e6007e"},
                    {"weight":"1"}]},
                {"featureType":"landscape",
                 "elementType":"all",
                 "stylers":[
                    // {"color":"#ffe146"},
                    {"color": "#ffc04c"},
                    {"saturation":"-28"},
                    {"lightness":"0"}]},
                {"featureType":"poi",
                 "elementType":"all",
                 "stylers":[
                    {"visibility":"off"}]},
                {"featureType":"road",
                 "elementType":"all",
                 "stylers":[
                    {"color":"#0096aa"},
                    {"visibility":"simplified"},
                    {"saturation":"-75"},
                    {"lightness":"5"},
                    {"gamma":"1"}]},
                {"featureType":"road",
                 "elementType":"labels.text",
                 "stylers":[
                    {"visibility":"on"},
                    {"color":"#ffc04c"},
                    {"weight":8},
                    {"saturation":"-28"},
                    {"lightness":"0"}]},
                {"featureType":"road",
                 "elementType":"labels.text.fill",
                 "stylers":[
                   {"visibility":"on"},
                   {"color":"#0096aa"},
                   {"weight":8},
                   {"lightness":"5"},
                   {"gamma":"1"},
                   {"saturation":"-75"}]},
                {"featureType":"road",
                 "elementType":"labels.icon",
                 "stylers":[
                   {"visibility":"off"}]},
                {"featureType":"transit",
                 "elementType":"all",
                 "stylers":[
                   {"visibility":"simplified"},
                   {"color":"#0096aa"},
                   {"saturation":"-75"},
                   {"lightness":"5"},{"gamma":"1"}]},
                {"featureType":"water",
                 "elementType":"geometry.fill",
                 "stylers":[
                   {"visibility":"on"},
                   {"color":"#0096aa"},
                   {"saturation":"-75"},
                   {"lightness":"5"},
                   {"gamma":"1"}]},
                {"featureType":"water",
                 "elementType":"labels.text",
                 "stylers":[
                   {"visibility":"simplified"},
                   {"color":"#ffc04c"},
                   {"saturation":"-28"},
                   {"lightness":"0"}]},
                {"featureType":"water",
                 "elementType":"labels.icon",
                 "stylers":[{"visibility":"off"}]}];
  var styledMapOptions = {
    name: 'Simple'
  };
  var customMapType = new google.maps.StyledMapType(
        styles,
        styledMapOptions);
  var mapOptions = {
    // sets map center to the first item in places list 
    center: centerLatLng,
    zoom: 3,
    mapTypeControlOptions: {
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
      }
    };

  var infoWindow = new google.maps.InfoWindow({
    maxWidth: 75
    });
  

  map = new google.maps.Map(document.getElementById('my-map'), mapOptions);

  map.mapTypes.set('map_style', customMapType);
  map.setMapTypeId('map_style');

  var bounds = new google.maps.LatLngBounds();

  for (var i = 0; i < places.length; i++) {
    var latFromDom = $(places[i]).data('lat');
    var lngFromDom = $(places[i]).data('lng');
    var name = $(places[i]).data('name');
    var yelp = $(places[i]).data('yelp');
    var myLatLng = {lat: latFromDom, lng: lngFromDom};
    var contentString = '<div id="info">' +
    '<p>'+ name + '</p><p>' + yelp + ' stars ' + '</p>' + '<button class="uber btn" type="button" data-toggle="modal" data-target="#myModal" data-lat=' + "'" + latFromDom + "'" + 'data-lng=' + "'" + lngFromDom + "'" + '>Uber</button>';

    if (latFromDom, lngFromDom){
      addMarker(myLatLng, name);
      markers.push(marker);
    }

    bindInfoWindow(marker, map, infoWindow, contentString);
  }

  // TRYING TO FIX BUG WHERE MAP STARTS IN THE OCEAN
  if (markers.length > 0) {
    for (var j = 0; j < markers.length; j++) {
      bounds.extend(markers[j].getPosition());
    }
    map.fitBounds(bounds);
  }

  
}


google.maps.event.addDomListener(window, 'load', initMap);
