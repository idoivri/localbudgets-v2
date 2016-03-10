function getName(d) {
  if( d.name == 'root') {
    return "כללי";
  } else{
    return d.name;
  }
}

function colores_google(n) {
  var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}

var muni_color_scale;
var get_data= (function (muni,year) {

  var width = 1200,
  height = 550,
  radius = Math.min(width, height) / 2 - 10;

  var formatNumber = d3.format(",d");

  //ההיקף
  var x = d3.scale.linear()
  .range([0, 2 * Math.PI]);

  //העומק
  var y = d3.scale.sqrt()
  .range([0, radius]);

  var color =  d3.scale.category10();

  var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>" + getName(d) + "</strong> \
    <span style='color:red'>" + formatNumber(d.amount) + ' ש"ח' + "</span> <br>" +
    "<strong>" + "סעיף" + "</strong> \
    <span style='color:orange'>" + (d.code ? d.code : 'כל הסעיפים') + "</span>";
  })

  d3.select("svg").remove();

  var svg = d3.select("#auto_data").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");

  svg.call(tip);

  var partition = d3.layout.partition()
  .value(function(d) { return d.size; });

  var arc = d3.svg.arc()
  .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
  .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
  .innerRadius(function(d) { return Math.max(0, y(d.y)); })
  .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });


  $.get( '/api/v1/get_budget_tree',
  {
    muni : muni,
    year: year.toString()
  }
).done(
  function(root,error){

    var g = svg.selectAll("g")
    .data(partition.nodes(root))
    .enter().append("g");

    var path = svg.selectAll("path")
    .data(partition.nodes(root))
    .enter().append("path")
    .attr("d", arc)
    .style("fill", function(d) { return color( getName(d) ); })
    .on("click", click)
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

    function click(d) {
      path.transition()
      .duration(750)
      .attrTween("d", arcTween(d))
    }

    function computeTextRotation(d){
      return (x(d.x +d.dx /2) - Math.PI/2) / Math.PI * 180;
    }

    //legend  code
    var legendRectSize = 28;
    var legendSpacing = 8
    var legend = svg.selectAll('.legend')
    .data(
      data = partition.nodes(root).filter (function (d) {
        return (d.size > 0  &&  d.depth < 2) })
      )
      .enter()
      .append('g')
      .attr('class', 'legend')
      .attr('transform', function(d, i) {
        var height = legendRectSize + legendSpacing;
        var offset =  height * data.length / 2;
        var horz = radius + 200;
        var vert = i * height - offset;
        return 'translate(' + horz + ',' + vert + ')';
      });

      legend.append('rect')
      .attr('width', legendRectSize)
      .attr('height', legendRectSize)
      .style('fill', function(d) { return color(getName(d)) })
      .style('stroke', function(d) { return color(getName(d)) });

      legend.append('text')
      .attr('x', -10)
      .attr('y', legendRectSize - legendSpacing)
      .text(function(d) { return getName(d) ;});

      legend.on("mouseover",function (dLegend) {
        path
        .filter(function (d) { return d._id === dLegend._id })
        .call(function (selection) {
          selection[0][0].style.opacity = '0.7';
          tip.show(dLegend,selection[0][0])
        });
      }).on('mouseout',function (dLegend) {
        path
        .filter(function (d) { return d._id === dLegend._id })
        .call(function (selection) {
          selection[0][0].style.opacity = '1'
          tip.hide(dLegend,selection[0][0])
        });
      })

      legend.on("click",click)
    });

    // Interpolate the scales!
    function arcTween(d) {
      var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
      yd = d3.interpolate(y.domain(), [d.y, 1]),
      yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
      return function(d, i) {
        return i
        ? function(t) { return arc(d); }
        : function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
      };
    }
  })

  $(document).ready(function() {
    $(function(){
      $(".muni_name").on('click', function(){
        $("#muni_dropdown:first-child").html($(this).text() + "<span class=\"caret\"></span>");
        $("#muni_dropdown:first-child").val($(this).attr('id'));

        // Clear previous results
        $("#years_dropdown_vals").empty()
        //

        $.get('/api/v1/get_muni_year',
        {
          name : $(this).text()
        },
        function(result){
          years = $.parseJSON(result).res;
          //  alert(years)
          $.each(years, function(index, year){

            var item_wrapped = $('<li/>').append(
              $("<a/>").attr("id",year).text(year).addClass("muni_year").
              on('click', function(){
                $("#years_dropdown:first-child").html($(this).text() + "<span class=\"caret\"></span>");
                $("#years_dropdown:first-child").val($(this).text());
                $("#muni_go").removeClass("disabled");

              })
            );

            $("#years_dropdown_vals").append( item_wrapped ) ;
          });
        }
      );
      $("#years_dropdown").removeClass("disabled");
    });

    $("#muni_go").on('click', function(){
      get_data($("#muni_dropdown:first-child").val(), $("#years_dropdown:first-child").val() );
    });

    get_data('ashdod','2013')
  });
});
