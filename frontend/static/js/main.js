//TODO a hack until "תקציב עיריית X" would be supported in the server
function toggle_expense(){
    console.log('Bla')
    if( $("#muni_go").hasClass("disabled") ) { return; }
    get_data($("#muni_dropdown:first-child").val(), $("#years_dropdown:first-child").val() ,document.getElementById('muni_toggle_income_expense').checked);
    };


function getName(d) {
  if( d.name == 'root') {
    return "כללי";
  } else{
    return d.name;
  }
}

function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (arguments.length === 1) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}

function getColor(d) {
 var x = d3.scale.linear()
  .range([0, 2 * Math.PI]);
   var meanAngle = (Math.max(0, Math.min(2 * Math.PI, x(d.x)))+Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))))/2;
//    console.log(meanAngle);
    var hsv2rgb = HSVtoRGB(meanAngle/(Math.PI*2),0.63,0.65);
  return 'rgb('+ hsv2rgb.r +','+hsv2rgb.g +','+hsv2rgb.b +')'
}



function colores_google(n) {
  var colores_g =
  ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099",
  "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395",
  "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300",
  "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}


//Breadcrumbs

// Breadcrumb dimensions: width, height, spacing, width of tip/tail.
var b = {
  w: 150, h: 50, s: 5, t: 10
};

function initializeBreadcrumbTrail() {
  // Add the svg area.
  var trail = d3.select("#auto_breadcrumbs")
      .append("svg:svg")
      .attr("width", 1200)
      .attr("height", 50)
      .attr("id", "trail");
  // Add the label at the end, for the percentage.
  trail.append("svg:text")
    .attr("id", "endlabel")
    .style("fill", "#000");
};


/**
* fetches (muni,year) data from server
* and displays all relevant visualization
*/


function get_data(muni,year,expense) {

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

  var color =  getColor;

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
  // initializeBreadcrumbTrail();

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
    expense: expense // { 'income','expense','all' } whether to show income or expense budget
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
      .style("fill", function(d) { return color( d ); })
//      zoom on click
      .on("click", click)
      .on('mouseover', mouseover)
      .on('mouseout', mouseleave);


      function mouseover(d) {
        tip.show(d);

        var sequenceArray = getAncestors(d);
     //   updateBreadcrumbs(sequenceArray, "");

        // Fade all the segments.
        d3.selectAll("path")
            .style("opacity", 0.6);

        // Then highlight only those that are an ancestor of the current segment.
        svg.selectAll("path")
            .filter(function(node) {
                      return (sequenceArray.indexOf(node) >= 0);
                    })
            .style("opacity", 1);
      }

      // Restore everything to full opacity when moving off the visualization.
      function mouseleave(d) {
        tip.hide(d);
        // // Hide the breadcrumb trail
        // d3.select("#trail")
        //     .style("visibility", "hidden");

        // Deactivate all segments during transition.
        d3.selectAll("path").on("mouseover", null);

        // Transition each segment to full opacity and then reactivate it.
        d3.selectAll("path")
            .transition()
            .duration(100)
            .style("opacity", 1)
            .each("end", function() {
                    d3.select(this).on("mouseover", mouseover);
                  });

        d3.select("#explanation")
            .style("visibility", "hidden");
      }

      //zoom on clicked node, and animate transition
      function click(d) {
        path.transition()
        .duration(750)
        .attrTween("d", arcTween(d))
        showLegend(d);
      }
      showLegend(root);

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
        .style('fill', function(d) { return color(d) })
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


    // Given a node in a partition layout, return an array of all of its ancestor
    // nodes, highest first, but excluding the root.
    function getAncestors(node) {
      var path = [];
      var current = node;
      while (current.parent) {
        path.unshift(current);
        current = current.parent;
      }
      path.unshift(current);
      return path;
    }

    // Generate a string that describes the points of a breadcrumb polygon.
    function breadcrumbPoints(d, i) {
      var points = [];
      points.push("0,0");
      points.push(b.w + ",0");
      points.push(b.w + b.t + "," + (b.h / 2));
      points.push(b.w + "," + b.h);
      points.push("0," + b.h);
      if (i > 0) { // Leftmost breadcrumb; don't include 6th vertex.
        points.push(b.t + "," + (b.h / 2));
      }
      return points.join(" ");
    }

    // Update the breadcrumb trail to show the current sequence and percentage.
    function updateBreadcrumbs(nodeArray, percentageString) {

      // Data join; key function combines name and depth (= position in sequence).
      var g = d3.select("#trail")
          .selectAll("g")
          .data(nodeArray, function(d) { return d.name + d.depth; });

      // Add breadcrumb and label for entering nodes.
      var entering = g.enter().append("svg:g");

      entering.append("svg:polygon")
          .attr("points", breadcrumbPoints)
          .style("fill", function(d) { return getColor(d) });

      entering.append("svg:text")
          .attr("x", (b.w + b.t) / 2)
          .attr("y", b.h / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .text(function(d) { return d.name.split(" ")[0]; })
          .style('fill','white'); //TODO color should be white

      // Set position for entering and updating nodes.
      g.attr("transform", function(d, i) {
        return "translate(" + i * (b.w + b.s) + ", 0)";
      });

      // Remove exiting nodes.
      g.exit().remove();

      // Now move and update the percentage at the end.
      d3.select("#trail").select("#endlabel")
          .attr("x", (nodeArray.length + 0.5) * (b.w + b.s))
          .attr("y", b.h / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .text(percentageString);

      // Make the breadcrumb trail visible, if it's hidden.
      d3.select("#trail")
          .style("visibility", "");
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

        // Hack to make the first child the selection
        $("#years_dropdown:first-child").html("בחר שנה<span class=\"caret\"></span>");
        $("#muni_go").addClass("disabled");


        //get avliable years for this muni
        $.get('/api/v1/get_muni_roots',
        {
          name : $(this).attr('id')
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
      if( $("#muni_go").hasClass("disabled") ) { return; }
      get_data($("#muni_dropdown:first-child").val(), $("#years_dropdown:first-child").val() ,document.getElementById('muni_toggle_income_expense').checked);
    });


    //A default muni to display before user selects anything
    get_data('ashdod','2013')
  });
});
