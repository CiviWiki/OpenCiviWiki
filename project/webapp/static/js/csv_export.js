$(document).ready(function() {
  $('#csv-export').click(function() {
    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:8000/civi2csv',
      data: JSON.stringify({'thread': /[^/]*$/.exec(window.location.href)[0]})
    }).done(function(data) {
      $('#csv-download').attr({
        download: 'thread-' + /[^/]*$/.exec(window.location.href)[0] + '.csv',
        href: 'data:text/csv,' + data
      });
      document.getElementById('csv-download').click();
    }).fail(function(errorThrown) {console.log('Error:' + JSON.stringify(errorThrown))});
  });
});
