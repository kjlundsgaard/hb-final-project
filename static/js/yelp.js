"use strict";

function scheduleEventListerForRestaurantButtons(){
  $('.restaurant-button').click(addRestaurant);
}

function displayResults(data) {
    var text = "";
    for (var i = 0; i < data.results.length; i++){
      // DATA ATTRIBUTES FOR SENDING DATA TO SERVER
      text = text + "<button class='restaurant-button' id=" + "'" + i + "'" + 
                             "data-restaurant-name=" + "'" + data.results[i].name + "'" +
                             "data-yelp-rating=" + "'" + data.results[i].rating + "'" +
                             "data-latitude=" + "'" + data.results[i].latitude + "'" +
                             "data-longitude=" + "'" + data.results[i].longitude + "'" + ">" +
                      "<p>" + data.results[i].name + "</p>" +
                      "<p>" + data.results[i].rating + "</p>" +
                    "</button>";
    }
    $('#results').html(text);
    scheduleEventListerForRestaurantButtons();
}

function submitSearch(evt) {
    evt.preventDefault();
    var formInputs = {
        "location": $("#location").val(),
        "term": $("#term").val()
    };

    $.post("/search-restaurant.json",
           formInputs,
           displayResults
           );
}

$("#search").on("submit", submitSearch);


function addRestaurant(evt){

    var id = this.id; // this is the id on the button we clicked, which is the image's id
    var restaurant_name = $(this).data('restaurant-name');
    var yelp_rating = $(this).data('yelp-rating');
    var latitude = $(this).data('latitude');
    var longitude = $(this).data('longitude');
    var listId = $("#list-info").data('listid');

    $.post("/add-restaurant.json", {'id': id,
                               'restaurant_name': restaurant_name,
                               'yelp_rating': yelp_rating,
                               'latitude': latitude,
                               'longitude': longitude,
                               'list_id': listId},
                               addRestaurantSuccess);
    
}

function addRestaurantSuccess(result){

    console.log(result.status);

    var id = result.id;

    $('#' + id).css('color', 'red'); // give our user some feedback
}
