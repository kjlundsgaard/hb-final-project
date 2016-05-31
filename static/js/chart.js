Chart.defaults.global.defaultFontColor = '#000000';
var options = {
  responsive: true,
  legend: {
    display: false,
  },
  scales: {
        yAxes: [{
            display: true,
            ticks: {
                beginAtZero: true   // minimum value will be 0.
            }
        }]
    }
};

// Make Donut Chart of percent of different types of Melons
var ctx = $("#myChart").get(0).getContext("2d");

$.get("/categories.json", function (data) {
    var myDoughnutChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
    console.log(data.types);
});