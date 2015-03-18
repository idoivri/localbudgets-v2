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


var set_basic_search = (function(){
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

var set_advanced_search = (function(){
  $("#advanced_search_btn").click(function(){
    var formValues = $('#advanced_form').form('get values');
    var year = formValues.year;
    var city = formValues.city;
    var query = formValues.query;

    if(year=='' && city=='' && query==''){
      $("#form_warning").removeClass('hidden').addClass('visible');
      return;
    } else{
      $("#form_warning").removeClass('visible').addClass('hidden');
      $.get('/api/v1/lines',
              {
              city: city,
              year: year,
              query: query
              },
              parseTableRes,
              'json'
        );
    }
  });
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

  $("#advanced_search").click(function(){
    $("#advanced_search_form").attr('class', 'visible');
    $("#pie_chart").attr('class', 'hidden');
    $('.left.sidebar')
        .sidebar('toggle');
  });

  set_basic_search();
  set_advanced_search();
});
