//TODO a hack until "תקציב עיריית X" would be supported in the server
function getName(d) {
  if( d.name == 'root') {
    return "כללי";
  } else{
    return d.name;
  }
}

function colores_google(n) {
  var colores_g = 
  ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099",
  "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395",
  "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300",
  "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}

/**
* fetches (muni,year) data from server
* and displays all relevant visualization
*/
function get_data(muni,year) {

  //svg canvas dimensions
  var width = 1200,
  height = 550,

  // sunburst radius
  radius = Math.min(width, height) / 2 - 10;

  //format budget values
  var formatBudget = d3.format(",d");

  //scale perimeter
  var x = d3.scale.linear()
  .range([0, 2 * Math.PI]);

  //scale depth/width of arcs
  var y = d3.scale.sqrt()
  .range([0, radius]);

  var color =  d3.scale.category10();

  //define tip html
  var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>" + getName(d) + "</strong> \
    <span style='color:red'>" + formatBudget(d.amount) + ' ש"ח' + "</span> <br>" +
    "<strong>" + "סעיף" + "</strong> \
    <span style='color:orange'>" + (d.code ? d.code : 'כל הסעיפים') + "</span>";
  })

  //clean previous svg
  d3.select("svg").remove();

  //append new svg
  var svg = d3.select("#auto_data").append("svg")
  .attr("width", width)
  .attr("height", height)
  //group chart elements
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");

  svg.call(tip);

  //d3 partition layout, by size
  var partition = d3.layout.partition()
  .value(function(d) { return d.size; })
  .sort(function comparator(a, b) {
        return b.code - a.code;
  });

  //calculate arcs
  var arc = d3.svg.arc()
  .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
  .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
  .innerRadius(function(d) { return Math.max(0, y(d.y)); })
  .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

  //fetch data
  $.get( '/api/v1/get_budget_tree',
  {
    muni : muni, //which muni
    year: year.toString(), // which year
    budget: 'all' // { 'income','expense','all' } whether to show income or expense budget
  })
  .done(
    function(root,error){

      var nodes = partition.nodes(root);
      var clickedNode;

      //bind svg paths to budget nodes
      var path = svg.selectAll("path")
      .data(nodes)
      .enter()
      .append("path")
      //draw arcs
      .attr("d", arc)
      //color by name
      .style("fill", function(d) { return color( getName(d) ); })
      //zoom on click
      .on("click", click)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

      //zoom on clicked node, and animate transition
      function click(d) {
        path.transition()
        .duration(750)
        .attrTween("d", arcTween(d))

        showLegend(d)
      }

      //show legend with children of selected node
      function showLegend(d) {

        //legend  code
        var legendRectSize = 28;
        var legendSpacing = 8

        //clean previous legend
        d3.selectAll(".legend").remove();

        //bind budget nodes to legend
        var legend = svg.selectAll('.legend')
        .data(data = d.children)
        .enter()
        .append('g')
        .attr('class', 'legend')

        //position legend alongside chart
        .attr('transform', function(d, i) {
          var height = legendRectSize + legendSpacing;
          var offset =  height * data.length / 2;
          var horz = radius + 200;
          var vert = i * height - offset;
          return 'translate(' + horz + ',' + vert + ')';
        });
        //legend squares
        legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', function(d) { return color(getName(d)) })
        .style('stroke', function(d) { return color(getName(d)) });

        //legend labels
        legend.append('text')
        .attr('x', -10)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return getName(d) ;});

        //show tooltip on chart when mouseover legend
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
        //zoom chart when clicking legend
        legend.on("click",click)
      } //end of showLegend

    }); //end of visualization wrapper function

    //interpolate the scales
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
  }

  $(document).ready(function() {
    // Initialize Bootstrap Switch
    $("#muni_toggle_income_expense").bootstrapSwitch();
    $(function(){

      $(".muni_name").on('click', function(){

        //select muni
        $("#muni_dropdown:first-child").html($(this).text() + "<span class=\"caret\"></span>");
        $("#muni_dropdown:first-child").val($(this).attr('id'));

        // Clear previous results
        $("#years_dropdown_vals").empty()

        //get avliable years for this muni
        $.get('/api/v1/get_muni_year',
        {
          name : $(this).text()
        },
        function(result){
          years = $.parseJSON(result).res;
          $.each(years, function(index, year){

            //update years dropdown
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

    // fetch and display chart
    // note that get_data also displays visualization
    $("#muni_go").on('click', function(){
      get_data($("#muni_dropdown:first-child").val(), $("#years_dropdown:first-child").val() );
    });

    //A default muni to display before user selects anything
    get_data('ashdod','2013')
  });
});
