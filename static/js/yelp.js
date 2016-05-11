"use strict";

function displayResults(data) {
    console.log(data);
    var text = "";
    for (var i = 0; i < data.results.length; i++){
      text = text + "<button class='restaurant-button' id=" + i + ">" +
      "<p id='restaurant_name'>" + data.results[i].name + "</p>" +
      "<p id='yelp_rating'>" + data.results[i].rating + "</p>" +
      "<span type='hidden' id='latitude' value="  + data.results[i].latitude + ">" + "</span>" +
      "<span type='hidden' id='latitude' value=" + data.results[i].latitude + ">" + "</span>" +
      "</button>";
    }
    $('#results').html(text);
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



$(function (){ // this is the jquery shortcut for document.ready()

    function addRestaurant(evt){

        var id = this.id; // this is the id on the button we clicked, which is the image's id

        $.post("/add-restaurant", {'id': id}, addRestaurantSuccess);
    }

    function addRestaurantSuccess(result){

        console.log(result.status);

        var id = result.id;

        $('#' + id).css('color', 'red'); // give our user some feedback
    }

    $('.restaurant-button').click(addRestaurant);

});