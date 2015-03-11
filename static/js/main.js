var jsonData = '['+
              '{"code": "1", "name": "bla", "amnt": "500"},'+
              '{"code":"32", "name":"bla2","amnt":"54"},'+
              '{"code":"3", "name":"בלה בלה","amnt":"54"}'+
            ']';

var parseTableRes = (function(data,status){
    var data = JSON.parse(jsonData);
    var innerHtml ='';
    var rowVal;
    $.each(data, function(i,item){
      rowVal = '<tr>'+
                  '<td>' + item.code + '</td>' +
                  '<td>' + item.name + '</td>' +
                  '<td>' + item.amnt + '</td>' +
                '</tr>';
      innerHtml += rowVal;
    });
    $("#table_body").append(innerHtml);
});


$(document).ready(function() {

  $('.ui.dropdown')
      .dropdown({
        on: 'hover'
  });

  $("#sidebar_opener").click(function(){
    $('.left.sidebar')
        .sidebar('toggle')
        .sidebar({
          context: $('.page.context .bottom.segment')
        })
        .sidebar('attach events', '.page.context .menu .item');
        // .sidebar('setting', 'transition', 'overlay');
  });
  // parseTableRes();
  $("#search_btn").click(function(){
    // alert("wwor");
    // var search_term = $("#search_general").text();
    parseTableRes();
    // $.get({
    //   url: '',
    //   type: 'GET',
    //   data: {
    //       city: ???
    //   },
    //   success: parseTableRes,
    //   dataType: 'json'
    // });
  });
});
