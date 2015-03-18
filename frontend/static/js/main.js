var parseTableRes = (function(data_res,status){
    var data = $.parseJSON(data_res).res;
    var innerHtml ='';
    var rowVal;
    $.each(data, function(i,item){
      rowVal = '<tr>'+
                  '<td>' + item.code + '</td>' +
                  '<td>' + item.name + '</td>' +
                  '<td>' + item.amount + '</td>' +
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
  $("#search_btn").click(function(){

    var search_term = $("#search_general").val();

    $.get('/api/v1/lines',
          {
          code: search_term
          },
          parseTableRes,
          'json'
    );
  });
});
