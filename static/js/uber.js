var userLat;
var userLng;
var endLat;
var endLng;

navigator.geolocation.watchPosition(function(position) {
    // Update user's latitude and longitude
    console.log(position);
    userLat = position.coords.latitude;
    userLng = position.coords.longitude;
});

function sendLocationToServerForEstimates(evt) {
    console.log('in sending function');
    $.post('/get-uber-data.json',
        { 'start_latitude': userLat,
        'start_longitude': userLng,
        'end_latitude': endLat,
        'end_longitude': endLng})
        .done( getUberResults )
        .fail( priceInfoUnavailable );
}

function updateEndLatLng(evt) {
    endLat = $(this).data('lat');
    endLng = $(this).data('lng');

    sendLocationToServerForEstimates();
}

function getUberResults(data) {
    console.log(data.results);
    resultText = "";
    results = data.results;
    for (var i = 0; i < results.length; i++) {
        resultText = resultText + "<p><b>" + results[i].car + "</b></p><p>Ride Duration " + results[i].duration + " minutes | Distance: " + results[i].distance + " miles | Price: " + results[i].price_estimate + "</p>";
    }

    $('#uber-info').html(resultText);
}

function scheduleEventListenerForUber() {
    $('.uber').click(updateEndLatLng);
}

function priceInfoUnavailable() {
    $('#uber-info').html("Sorry, we could not get price info from your location");
}