"use strict";

// This goes at the top because it needs to be defined to get called when results are displayed
function scheduleEventListerForRestaurantButtons(){
  // 
  // $('.restaurant-button').click(showRestaurantInfo);
  $('.add-button').click(addRestaurant);

}

// AJAX to display results of query using Yelp API response
function displayResults(data) {
    var text = "";
    for (var i = 0; i < data.results.length; i++){
      text = text + "<button class='restaurant-button btn' type='button'id=" + "'button" + i + "'" + 
                             "data-restaurant-name=" + '"' + data.results[i].name + '"' +
                             "data-yelp-rating=" + "'" + data.results[i].rating + "'" +
                             "data-address=" + "'" + data.results[i].address + "'" +
                             "data-categories=" + "'" + data.results[i].categories + "'" +
                             "data-neighborhoods=" + '"' + data.results[i].neighborhoods + '"' +
                             "data-latitude=" + "'" + data.results[i].latitude + "'" +
                             "data-longitude=" + "'" + data.results[i].longitude + "'" + 
                             "data-url=" + "'" + data.results[i].url + "'" + 
                             ">" +
                      "<span>" + data.results[i].name + "</span>" + 
                    "</button>";
    }
    $('#yelpResultsPanel').removeClass('hidden');
    $('#results').html(text);


    $('.restaurant-button').click(function() {
      var name = $(this).data('restaurant-name');
      var yelp = $(this).data('yelp-rating');
      var address = $(this).data('address');
      var categories = $(this).data('categories');
      var neighborhoods = $(this).data('neighborhoods') ? ($(this).data('neighborhoods')).split(",") : null;
      var latitude = $(this).data('latitude');
      var longitude = $(this).data('longitude');
      var url = $(this).data('url');
      var infobox = "<table class='table'><tr><td class='title'>" + name + "</td></tr>" + 
                             "<tr><td class='title'>Yelp Rating: " + yelp + "</td></tr>" + 
                             "<tr><td class='title'>Address: " + address + "</td></tr>" + 
                             "<tr><td class='title'>Neighborhood: " + ( neighborhoods ? neighborhoods.join(", ") : "None" ) + 
                             "</td></tr></table>" + 
                             "<button type='button' class='add-button btn' id='button' " + 
                             "data-restaurant-name=" + '"' + name + '"' +
                             "data-yelp-rating=" + "'" + yelp + "'" +
                             "data-address=" + "'" + address + "'" +
                             "data-categories=" + "'" + categories + "'" +
                             "data-neighborhoods=" + '"' + neighborhoods + '"' +
                             "data-latitude=" + "'" + latitude + "'" +
                             "data-longitude=" + "'" + longitude + "'" +
                             "data-url=" + "'" + url + "'" + ">" +
                             "Add " + name +"</button>";
      console.log(infobox);
      $('#infobox').removeClass('hidden').html(infobox);
      var latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      // TRYING TO MAKE IT SUCH THAT THE MARKER GETS ADDED AND THEN DISAPPEARS WHEN ANOTHER YELP RESULT IS CLICKED
      var lastMarker = markers[markers.length - 1];
      if (lastMarker && lastMarker.icon === otherIcon) {
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
      $(this).addClass('btn-info');
      $('#my-map').addClass('small');
    })
    // gives access to the add restaurant event listener once items are loaded
}

function submitSearch(evt) {
    evt.preventDefault();
    var formInputs = {
        "location": $("#location").val(),
        "term": $("#term").val()
    };
    $('#yelpResultsPanel').removeClass('hidden');
    $('#results').html("searching...");;
    $.post("/search-restaurant.json",
           formInputs,
           displayResults
           );
}

$("#search").on("submit", submitSearch);

// sends restaurant data to server to add restaurant to list
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
    var url = $(this).data('url');

    console.log(restaurantName);

    $.post("/add-restaurant.json", {'id': id,
                               'restaurant_name': restaurantName,
                               'yelp_rating': yelp_rating,
                               'latitude': latitude,
                               'longitude': longitude,
                               'list_id': listId,
                               'address': address,
                               'categories': categories,
                               'neighborhoods': neighborhoods,
                               'url': url},
                               getRestaurantsFromDB);

    $('.add-button').html("Added!");
    
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

    $('.add-button').addClass('btn-success');

    // JUST TESTING OUT SOME PAGE RELOAD STUFF 
    // window.location.reload();
    var listings = "";

    for (var i = 0; i < data.results.length; i++) {
      listings = listings + 
      "<li id=" + "'" + data.results[i].restaurant_id + "'" + 
      " data-lat="+ "'" + data.results[i].latitude + "'" + 
      " data-lng=" + "'" + data.results[i].longitude + "'" + 
      " data-name="+ '"' + data.results[i].restaurant_name + '"' + 
      " data-yelp="+ "'" + data.results[i].yelp_rating + "'" + ">" +
      "<button class='remove-restaurant btn btn-danger' type='button' data-restid=" + 
      "'" + data.results[i].restaurant_id + "'" + ">X</button>" +
      "<button class='visited-restaurant btn btn-warning' type='button' data-restid=" + 
      "'" + data.results[i].restaurant_id + "'"+ ">Visited</button>" +
      data.results[i].restaurant_name + "</li>";
    }
    // console.log(listings);
    $('#restaurant-list').html(listings);
    $(".remove-restaurant").click(removeRestaurant);
    $(".star-restaurant").click(starRestaurant);
    $(".visited-restaurant").click(markAsVisited);
    initMap();
}

// #######################################################################
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

// ###############################################################
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

// ################################################################
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

// ################################################################
// STAR RESTAURANT FUNCTIONS

function starRestaurantSuccess(result){

    console.log(result.status);

    var id = result.id;

    $('#'+ id + '.star-restaurant').toggleClass("starred"); // give our user some feedback
}

function starRestaurant(evt){

    var restId = $(this).data('restid');

    console.log("in star restaurant function")

    $.post("/star-restaurant.json", {'rest_id': restId},
                               starRestaurantSuccess);
    
}

$('.star-restaurant').click(starRestaurant);

// ###################################################################
// marks a restaurant as visited

function markAsVisitedSuccess(data) {
  var id = data.id;

  // $('#' + id).css('color', 'red');
  window.location.reload();
}

function markAsVisited(evt) {
  var restId = $(this).data('restid');
  var listId = $('#restaurant-list').data('listid');

  console.log("in markAsVisited function");

  $.post("/mark-visited.json", {'rest_id': restId, 'list_id': listId},
                          markAsVisitedSuccess);
}

$(".visited-restaurant").click(markAsVisited);

// #################################################################
