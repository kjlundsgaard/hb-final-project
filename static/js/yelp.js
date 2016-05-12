"use strict";

// This goes at the top because it needs to be defined to get called when results are displayed
function scheduleEventListerForRestaurantButtons(){
  $('.restaurant-button').click(addRestaurant);
}

// AJAX to display results of query using Yelp API response
function displayResults(data) {
    var text = "";
    for (var i = 0; i < data.results.length; i++){
      // DATA ATTRIBUTES FOR SENDING DATA TO SERVER
      text = text + "<button class='restaurant-button' id=" + "'" + i + "'" + 
                             "data-restaurant-name=" + '"' + data.results[i].name + '"' +
                             "data-yelp-rating=" + "'" + data.results[i].rating + "'" +
                             "data-latitude=" + "'" + data.results[i].latitude + "'" +
                             "data-longitude=" + "'" + data.results[i].longitude + "'" + ">" +
                      "<p>" + data.results[i].name + "</p>" +
                      "<p>" + data.results[i].rating + "</p>" +
                    "</button>";
    }
    $('#results').html(text);
    // gives access to the add restaurant event listener once items are loaded
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

// sends restaurant data to serve to add restaurant to list
function addRestaurant(evt){

    var id = this.id; // this is the id on the button we clicked, which is the image's id
    var restaurantName = $(this).data('restaurant-name');
    var yelp_rating = $(this).data('yelp-rating');
    var latitude = $(this).data('latitude');
    var longitude = $(this).data('longitude');
    var listId = $("#list-info").data('listid');

    console.log(restaurantName);

    $.post("/add-restaurant.json", {'id': id,
                               'restaurant_name': restaurantName,
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

// AJAX TO REMOVE RESTAURANTS FROM LIST
// BROKEN I GUESS FIX ME PLEASE

function removeRestaurantSuccess(result) {
    console.log(result.status);
}

function removeRestaurant(evt) {
    console.log("made it to the function");
    var remove = confirm("are you sure you want to remove this restaurant?")
    console.log(remove);

    var restaurantId = $(this).data('restid');
    var listId = $("#list-info").data('listid');

    if (remove) {
      $.post("/delete-restaurant.json", {'restaurant_id': restaurantId,
                                 'list_id': listId},
                                  removeRestaurantSuccess);
    }

}

$(".remove-restaurant").click(removeRestaurant);

