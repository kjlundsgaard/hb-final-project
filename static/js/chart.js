Chart.defaults.global.defaultFontColor = '#000000';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontFamily = "'Quando', serif";
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
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
    console.log(data.types);
});