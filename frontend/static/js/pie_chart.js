
function create_chart (data) {

  $('#pie_chart').highcharts({
      chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          backgroundColor: 'rgba(255, 255, 255, .4)'
      },
      title: {
          text: 'Browser market shares at a specific website, 2014'
      },
      tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
          pie: {
              allowPointSelect: true,
              cursor: 'pointer',
              dataLabels: {
                  enabled: true,
                  format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                  style: {
                      color: 'black'
                  }
              }
          }
      },
      series: data
  });
}



// simulate result from ajax request... / data from server (should we use handlebars?)
$(document).ready(function() {
  res_data = [{
      type: 'pie',
      name: 'Browser share',
      data: [
          ['Firefox',   45.0],
          ['IE',       26.8],
          {
              name: 'Chrome',
              y: 12.8,
              sliced: true,
              selected: true
          },
          ['Safari',    8.5],
          ['Opera',     6.2],
          ['Others',   0.7]
      ]
  }];
  create_chart(res_data);
});
