var options = {
  responsive: true
};

// Make Donut Chart of percent of different types of Melons
var ctx = $("#myChart").get(0).getContext("2d");

$.get("/categories.json", function (data) {
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options
    });
    console.log(data.types);
  $('#chart-legend').html(myDonutChart.generateLegend());
});