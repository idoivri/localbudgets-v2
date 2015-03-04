var jsonData = '['+
              '{"code": "1", "name": "bla", "amnt": "500"},'+
              '{"code":"3", "name":"bla2","amnt":"54"}'+
            ']';

var parseTableRes = (function(data){
    var data = JSON.parse(jsonData);
    var innerHtml = '<tbody>';
    var rowVal;
    $.each(data, function(i,item){
      rowVal = '<tr>'+
                  '<td>' + item.code + '</td>' +
                  '<td>' + item.name + '</td>' +
                  '<td>' + item.amnt + '</td>' +
                '</tr>';
      innerHtml += rowVal;
    });
    innerHtml += '</tbody>';
    $("#res_table_bla").append(innerHtml);
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
  $("#blablabla").click(function(){
    // alert("wwor");
    parseTableRes();
    // $.ajax({
    //   url: '/echo/json/',
    //   type: 'POST',
    //   data: {
    //       json: jsonData
    //   },
    //   success: parseTableRes,
    //   error: function(a,status,err){ alert(err);}
    // });
  });
});
