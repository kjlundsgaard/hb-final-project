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
      text = text + "<button class='restaurant-button' id=" + "'button" + i + "'" + 
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
    var restaurantName = result.restaurant_name
    var yelpRating =result.yelp_rating
    var RestaurantId = result.restaurant_id

    var newListing = "<li class='restaurant-listing'>" + restaurantName + " | Yelp Rating: " + yelpRating + "</li>";

    $('#button' + id).css('color', 'red'); // give our user some feedback

    $('.restaurant-listing').append(newListing);
}

// sends restaurant id and list id to server to remove restaurant from list
function removeRestaurantSuccess(result) {
    console.log(result.status);
}

function removeRestaurant(evt) {
    var remove = confirm("are you sure you want to remove this restaurant?")

    var restaurantId = $(this).data('restid');
    var listId = $("#list-info").data('listid');

    if (remove) {
      $.post("/delete-restaurant.json", {'restaurant_id': restaurantId,
                                 'list_id': listId},
                                  removeRestaurantSuccess);
    }

}

$(".remove-restaurant").click(removeRestaurant);


// sends list info to server to remove list
function removeListSuccess(result) {
    console.log(result.status);
}

function removeList(evt) {
    console.log("made it to the function");
    var remove = confirm("are you sure you want to remove this category?")
    console.log(remove);

    var listId = $(this).data('listid');

    if (remove) {
      $.post("/delete-list.json", {'list_id': listId},
                                  removeListSuccess);
    }

}

$(".remove-list").click(removeList);

// sends group info to server to remove user from group
function leaveGroupSuccess(result) {
    console.log(result.status);
}

function leaveGroup(evt) {
    console.log("made it to the function");
    var remove = confirm("are you sure you want to leave this group?")
    console.log(remove);

    var groupId = $(this).data('groupid');

    if (remove) {
      $.post("/leave-group", {'group_id': groupId},
                                  leaveGroupSuccess);
    }

}

$(".leave-group").click(leaveGroup);


function starRestaurantSuccess(result){

    console.log(result.status);

    var id = result.id;

    $('#' + id).css('color', 'red'); // give our user some feedback
}

function starRestaurant(evt){

    var restId = $(this).data('restid');

    console.log("in star restaurant function")

    $.post("/star-restaurant.json", {'rest_id': restId},
                               starRestaurantSuccess);
    
}

$('.star-restaurant').click(starRestaurant);


