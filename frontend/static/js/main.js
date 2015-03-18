var empty_table = (function(){ $("#table_body").empty(); });

var set_table = (function(innerHtml){
  $("#table_body").append(innerHtml);
  $('#res_table_bla').tablesort();
  $('#res_table_bla thead th.number').data('sortBy', function(th, td, sorter) {
			return parseInt(td.text(), 10);
		});

});
var parseTableRes = (function(data_res,status){
    var data = $.parseJSON(data_res).res;
    var innerHtml ='';
    var rowVal;
    empty_table();
    $.each(data, function(i,item){
      rowVal = '<tr>'+
                  '<td>' + item.muni + '</td>' +
                  '<td>' + item.year + '</td>' +
                  '<td>' + item.code + '</td>' +
                  '<td>' + item.name + '</td>' +
                  '<td>' + item.amount + '</td>' +
                '</tr>';
      innerHtml += rowVal;
    });
    set_table(innerHtml);
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
        });
        //.sidebar('attach events', '.page.context .menu .item');
        // .sidebar('setting', 'transition', 'overlay');
  });
  $("#search_btn").click(function(){

    var search_term = $("#search_general").val();
    if(search_term.trim() == ""){
      empty_table();
      return;
    }
    $.get('/api/v1/lines',
          {
          term: search_term
          },
          parseTableRes,
          'json'
    );
  });
});
