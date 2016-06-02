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
        'end_longitude': endLng}, getUberResults);
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
    if (data.results) {
        for (var i = 0; i < results.length; i++) {
            resultText = resultText +
            "<tr><td>" + results[i].car + "</td>" +
            "<td>" + results[i].duration + " minutes</td>" +
            "<td>" + results[i].distance + " miles</td>" +
            "<td>" + results[i].price_estimate + "</td></tr>";
        }
    }
    else {
        resultText = "Sorry, we could not get price info from your location";
    }
    $('#uber-info').removeClass('hidden').html(resultText);

}

function scheduleEventListenerForUber() {
    $('.uber').click(updateEndLatLng);
}

function priceInfoUnavailable() {
    $('#uber-info').html("Sorry, we could not get price info from your location");
}