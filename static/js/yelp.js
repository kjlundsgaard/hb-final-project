"use strict";

// This goes at the top because it needs to be defined to get called when results are displayed
function scheduleEventListerForRestaurantButtons(){
  // 
  // $('.restaurant-button').click(showRestaurantInfo);
  $('.add-button').click(addRestaurant);

}

// beginning display box of restaurant info that should also have the add restauarant button
// function showRestaurantInfo() {
//   var infobox = "HELLOOOOOO<button class='add-button' id='button'>Add restaurant</button>";
//   $('#infobox').html(infobox);
//   $('.add-button').click(addRestaurant);
// }
// AJAX to display results of query using Yelp API response
function displayResults(data) {
    var text = "";
    for (var i = 0; i < data.results.length; i++){
      text = text + "<button class='restaurant-button' id=" + "'button" + i + "'" + 
                             "data-restaurant-name=" + '"' + data.results[i].name + '"' +
                             "data-yelp-rating=" + "'" + data.results[i].rating + "'" +
                             "data-address=" + "'" + data.results[i].address + "'" +
                             "data-categories=" + "'" + data.results[i].categories + "'" +
                             "data-neighborhoods=" + "'" + data.results[i].neighborhoods + "'" +
                             "data-latitude=" + "'" + data.results[i].latitude + "'" +
                             "data-longitude=" + "'" + data.results[i].longitude + "'" + ">" +
                      "<p>" + data.results[i].name + "</p>" + 
                    "</button>";
    }
    $('#results').html(text);

    $('.restaurant-button').click(function() {
      var name = $(this).data('restaurant-name');
      var yelp = $(this).data('yelp-rating');
      var address = $(this).data('address');
      var categories = $(this).data('categories');
      var neighborhoods = $(this).data('neighborhoods');
      var latitude = $(this).data('latitude');
      var longitude = $(this).data('longitude');
      var infobox = "<div class='infobox'><p>" + $(this).data('restaurant-name') + "</p>" + "<p> Yelp Rating: " + $(this).data('yelp-rating') + "</p>" + "<p> Address: " + $(this).data('address') + "</p>" + "<p> Neighborhood: " + $(this).data('neighborhoods') + "</p>" + "<button class='add-button' id='button' " + "data-restaurant-name=" + '"' + name + '"' +
                             "data-yelp-rating=" + "'" + yelp + "'" +
                             "data-address=" + "'" + address + "'" +
                             "data-categories=" + "'" + categories + "'" +
                             "data-neighborhoods=" + "'" + neighborhoods + "'" +
                             "data-latitude=" + "'" + latitude + "'" +
                             "data-longitude=" + "'" + longitude + "'" + ">" +
      "Add " + $(this).data('restaurant-name') + "</button></div>";
      $('#infobox').html(infobox);
      var latlng = {lat: latitude, lng: longitude};
      // TRYING TO MAKE IT SUCH THAT THE MARKER GETS ADDED AND THEN DISAPPEARS WHEN ANOTHER YELP RESULT IS CLICKED
      var lastMarker = markers[markers.length - 1];
      if (lastMarker.icon === otherIcon) {
        lastMarker.setMap(null);
        markers.pop();
      }
      initMap();
      addMarker(latlng, name, otherIcon);
      markers.push(marker);
      for (var j = 0; j < markers.length; j++) {
        bounds.extend(markers[j].getPosition());
      }
      map.fitBounds(bounds);
      scheduleEventListerForRestaurantButtons();
    })
    // gives access to the add restaurant event listener once items are loaded
}

function submitSearch(evt) {
    evt.preventDefault();
    var formInputs = {
        "location": $("#location").val(),
        "term": $("#term").val()
    };

    $('#results').html("searching...");;
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
    var address = $(this).data('address');
    var categories = $(this).data('categories');
    var neighborhoods = $(this).data('neighborhoods');

    console.log(restaurantName);

    $.post("/add-restaurant.json", {'id': id,
                               'restaurant_name': restaurantName,
                               'yelp_rating': yelp_rating,
                               'latitude': latitude,
                               'longitude': longitude,
                               'list_id': listId,
                               'address': address,
                               'categories': categories,
                               'neighborhoods': neighborhoods},
                               getRestaurantsFromDB);
    
}


// ########################################################################

function getRestaurantsFromDB(data){
  var listId = $('#list-info').data('listid');
  var id = data.id;
  console.log("in the get restaurants from db function");
  $.post('/return-restaurants.json', {'list_id': listId, 'id':id}, addRestaurantToDBsuccess);

}

function addRestaurantToDBsuccess(data){

    console.log(data.status);
    var id = data.id;

    $('#' + id).css('color', 'red');

    var listings = "";

    for (var i = 0; i < data.results.length; i++) {
      listings = listings + "<li id=" + "'" + data.results[i].restaurant_id + "'" + " data-lat="+ "'" + data.results[i].latitude + "'" + " data-lng=" + "'" + data.results[i].longitude + "'" + " data-name="+ '"' + data.results[i].restaurant_name + '"' + " data-yelp="+ "'" + data.results[i].yelp_rating + "'" + ">" + data.results[i].restaurant_name + " | Yelp Rating: " + data.results[i].yelp_rating + "<button class='remove-restaurant' data-restid=" + "'" + data.results[i].restaurant_id + "'" + ">Remove</button><button class='star-restaurant' id=" + "'" + data.results[i].restaurant_id + "'" + " data-restid=" + "'" + data.results[i].restaurant_id + "'" + ">LIKE</button></li>";
    }
    // console.log(listings);
    $('#restaurant-list').html(listings);
    // trying to get google maps to init map with markers when new listing is added
    // make separate addMarker function and use here
    // todo
    $(".remove-restaurant").click(removeRestaurant);
    initMap();
}

// sends restaurant id and list id to server to remove restaurant from list
function removeRestaurantSuccess(result) {
    console.log(result.status);
    window.location.reload();

}

function removeRestaurant(evt) {
    console.log('in remove function')
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
    window.location.reload();

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
    window.location.reload();
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


