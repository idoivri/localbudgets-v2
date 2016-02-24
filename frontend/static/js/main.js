var set_autocomplete = (function (is_disabled){
  $("#search_input").autocomplete({
    disabled : is_disabled,
    search: function(event, ui) {
        $('#auto_data').empty();
    },
    source : "/api/v1/get_autocomplete",

  }).data('ui-autocomplete')._renderMenu = (function(ul,items){

    $.each(items, function(index, item){
      var res_data = $.parseJSON(item.value);
      console.log(res_data);

      //Populate items in a list
      var item_wrapped = $('<li/>')
       .attr("title", res_data.muni)
        .append(
        $("<span/>").addClass("value").attr("data-number", res_data.muni)
        .add(
            $("<span/>").text(res_data.muni).addClass("number")
          )
        );
      $('#auto_data').append(item_wrapped);


      var item_wrapped = $('<li/>')
       .attr("title", res_data.muni)
       .append(
              $("<span/>").addClass("bar").attr("data-number", res_data.amount)
              .add(
                  $("<span/>").text(res_data.amount).addClass("number")
                )
              );
      $('#auto_data').append(item_wrapped);

      var item_wrapped = $('<li/>')
       .attr("title", res_data.muni)
        .append(
        $("<span/>").addClass("value").attr("data-numnber", res_data.code)
        .add(
            $("<span/>").text(res_data.code).addClass("number")
          )
        );
      $('#auto_data').append(item_wrapped);

      var item_wrapped = $('<li/>')
       .attr("title", res_data.muni)
        .append(
        $("<span/>").addClass("value").attr("data-number", res_data.name)
        .add(
            $("<span/>").text(res_data.name).addClass("number")
          )
        );
      $('#auto_data').append(item_wrapped);

      var item_wrapped = $('<li/>')
       .attr("title", res_data.muni)
        .append(
        $("<span/>").addClass("value").attr("data-number", res_data.year)
        .add(
            $("<span/>").text(res_data.year).addClass("number")
          )
        );
      $('#auto_data').append(item_wrapped).append('<br/>');


    });
    $('.chart').horizBarChart();
  });
  //
  // $("#search_input").data('ui-autocomplete')._renderItem = (function(ul, item) {
  //
  //
  //
  //   return
  //  });
  //
  // .data('ui-autocomplete')._renderItem = function(ul, item) {
  //
  //   var res_data = $.parseJSON(item.value);
  //
  //   return $('<li/>')
  //    .data('item.autocomplete', item)
  //    .append(
  //           $("<span/>").addClass("bar").attr("data-number",res_data.amount)
  //           .add(
  //               $("<span/>").text(res_data.amount).addClass("number")
  //
  //             )
  //           )
  //    .appendTo($('#auto_data'));
  //  };

});

var set_basic_search = (function(){
  // $("#search_btn").click(function(){
  //
  //   var search_term = $("#search_general").val();
  //   if(search_term.trim() == ""){
  //     // empty_table();
  //     return;
  //   }
  //   $.get('/api/v1/get_query_result',
  //         {
  //           advanced : false,
  //           term: search_term
  //         }
  //   );
  // });



});

//
// var set_advanced_search = (function(){
//   $("#advanced_search_btn").click(function(){
//     var formValues = $('#advanced_form').form('get values');
//     var year = formValues.year;
//     var city = formValues.city;
//     var query = formValues.query;
//
//     if(year=='' && city=='' && query==''){
//       $("#form_warning").removeClass('hidden').addClass('visible');
//       return;
//     } else{
//       $("#form_warning").removeClass('visible').addClass('hidden');
//       $.get('/api/v1/lines',
//               {
//               city: city,
//               year: year,
//               query: query,
//               advanced : true
//               },
//               parseTableRes,
//               'json'
//         );
//     }
//   });
// });

var muni_color_scale;
var get_data= (function (muni,year) {
  // var width = 960,
  // height = 960,
  // radius = (Math.min(width, height) / 2) - 10;

  var width = 550,
      height = 550,
      radius = Math.min(width, height) / 2 - 10;

  var formatNumber = d3.format(",d");

  //ההיקף
  var x = d3.scale.linear()
  .range([0, 2 * Math.PI]);

  //העומק
  var y = d3.scale.sqrt()
  .range([0, radius]);

  var color = d3.scale.category20c();
  var color = d3.scale.ordinal().range(
    ['#50514f','#f25f5c','#ffe066','#247ba0','#70c1b3']);
    (['rgb(228,26,28)','rgb(55,126,184)','rgb(77,175,74)',
    'rgb(152,78,163)','rgb(255,127,0)','rgb(255,255,51)',
    'rgb(166,86,40)','rgb(247,129,191)','rgb(153,153,153)'])
  // var partition = d3.layout.partition()
  // .value(function(d) {
  //   return d.amount;
  // });

  // var arc = d3.svg.arc()
  // .startAngle(function(d) {
  //   return Math.max(0, Math.min(2 * Math.PI, x(d.x)));
  // })
  // .endAngle(function(d) {
  //   return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx)));
  // })
  // .innerRadius(function(d) {
  //   return Math.max(0, y(d.y));
  // })
  // .outerRadius(function(d) {
  //   return Math.max(0, y(d.y + d.dy));
  // });

  var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>" + (d.name == 'root' ? 'חורה' : d.name) + "</strong> \
            <span style='color:red'>" + formatNumber(d.amount) + ' ש"ח' + "</span> <br>" +
            "<strong>" + "סעיף" + "</strong> \
            <span style='color:orange'>" + (d.code ? d.code : 'כל הסעיפים') + "</span>";
  })

  // var svg = d3.select("body").append("svg")
  // .attr("width", width)
  // .attr("height", height)
  // .append("g")
  // .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");
  //
  // svg.call(tip);
  // d3.json("get_budget_tree.json", function(error, root) {
  //   if (error) throw error;
  //
  //   svg.selectAll("path")
  //   .data(partition.nodes(root))
  //   .enter().append("path")
  //   .attr("d", arc)
  //   .style("fill", function fill(d) {
  //     //return d3.rgb(d.depth * (256/4),0,(d.code ? d.code[0] : 0) * 256/9);
  //     return (d.depth ? color(getDepthOneAncestor(d).code) : "wheat");
  //   })
  //   //.style("opacity", function opacity(d) {
  //     // return 1 - d.depth/10;
  //   //})
  //   //.style("opacity:hover",0.5)
  //   .on("click", click)
  //   .on('mouseover', tip.show)
  //   .on('mouseout', tip.hide)
  //
  //   //remove native tooltip
  //   // .append("title")
  //   // .text(function(d) {
  //   //   return d.name + "\n" + formatNumber(d.value) + "\nקוד: " + d.code;
  //   // });
  // });

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
          .style("fill", function(d) { return color( d.name); })
          .on("click", click)
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide);

          path.append("title")
          .text(function(d) {
             return d.name + "\n" + d.amount +"\n" + "קוד:" + d.code;
           });

      var text = g.append("text")
        .attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
        .attr("x", function(d) { return y(d.y); })
        .attr("dx", "6") // margin
        .attr("dy", ".35em") // vertical-align
        .text(function(d) { return ""; }); //TODO I've deleted the text,
        //we should decide if that's good and remove the text related code from
        //this script

      function click(d) {
        // fade out all text elements
        // text.transition().attr("opacity", 0);

        path.transition()
          .duration(750)
          .attrTween("d", arcTween(d))
          .each("end", function(e, i) {
              // check if the animated element's data e lies within the visible angle span given in d
              if (e.x >= d.x && e.x < (d.x + d.dx)) {
                // get a selection of the associated text element
                var arcText = d3.select(this.parentNode).select("text");
                // fade in the text element and recalculate positions
                arcText.transition().duration(750)
                  .attr("opacity", 0)
                  .attr("transform", function() { return "rotate(" + computeTextRotation(e) + ")" })
                  .attr("x", function(d) { return y(d.y); });
              }
          });
      }
      function computeTextRotation(d){
        return (x(d.x +d.dx /2) - Math.PI/2) / Math.PI * 180;
      }
  });

  // d3.select(self.frameElement).style("height", height + "px");

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

  var get_data_old = (function(muni,year){
  var width = 550,
      height = 550,
      radius = Math.min(width, height) / 2 - 10;

  var x = d3.scale.linear()
      .range([0, 2 * Math.PI]);

  var y = d3.scale.sqrt()
      .range([0, radius]);

  var color = d3.scale.category20c();

  //d3.select("#auto_data svg").remove();

  var svg = d3.select("#auto_data").append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");

  var partition = d3.layout.partition()
      .value(function(d) { return d.size; });

  var arc = d3.svg.arc()
      .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
      .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
      .innerRadius(function(d) { return Math.max(0, y(d.y)); })
      .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

  // Helper method for choosing the fill color for the paths
  // finds the depth one Ancestor of given node
  function getDepthOneAncestor(node) {
        return node.depth > 1 ? getDepthOneAncestor(node.parent) : node;
  }
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
          .style("fill", function(d) { return color((d.children ? d : d.parent).name); })
          .on("click", click);

          path.append("title")
          .text(function(d) {
             return d.name + "\n" + d.amount +"\n" + "קוד:" + d.code;
           });

      var text = g.append("text")
        .attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
        .attr("x", function(d) { return y(d.y); })
        .attr("dx", "6") // margin
        .attr("dy", ".35em") // vertical-align
        .text(function(d) { return ""; }); //TODO I've deleted the text,
        //we should decide if that's good and remove the text related code from
        //this script

        function getDepthOneAncestor(node) {
          return node.depth > 1 ? getDepthOneAncestor(node.parent) : node;
        }

      function click(d) {
        // fade out all text elements
        // text.transition().attr("opacity", 0);

        path.transition()
          .duration(750)
          .attrTween("d", arcTween(d))
          .each("end", function(e, i) {
              // check if the animated element's data e lies within the visible angle span given in d
              if (e.x >= d.x && e.x < (d.x + d.dx)) {
                // get a selection of the associated text element
                var arcText = d3.select(this.parentNode).select("text");
                // fade in the text element and recalculate positions
                arcText.transition().duration(750)
                  .attr("opacity", 0)
                  .attr("transform", function() { return "rotate(" + computeTextRotation(e) + ")" })
                  .attr("x", function(d) { return y(d.y); });
              }
          });
      }
      function computeTextRotation(d){
        return (x(d.x +d.dx /2) - Math.PI/2) / Math.PI * 180;
      }
  });

  // d3.select(self.frameElement).style("height", height + "px");

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

});

$(document).ready(function() {

  $(function(){

      // muni_color_scale = {
      //
      // }

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

  });
  //
  // set_autocomplete(true);
  //
  // $('#search_type.btn-group').click(function(){
  //
  //    var search = $('#search_type .btn-group .active').attr("id");
  //
  //    if(search === "static_search"){
  //      set_autocomplete(true);
  //      $('#auto_data').empty();
  //    } else{
  //      set_autocomplete(false);
  //    }
  // })




  //
  // $("#advanced_search").click(function(){
  //   $("#advanced_search_form").attr('class', 'visible');
  //   $("#pie_chart").attr('class', 'hidden');
  //   $('.left.sidebar')
  //       .sidebar('toggle');
  // });

  // set_basic_search();
  //set_advanced_search();
});
