let firstlayeradded = false;
var files;

function update_wmslayer() {
  if( !$('#server-input').val() || !$('#file-path-input').val() || !$('#variable-input').val()) {
    alert('Please provide the needed values.');
  } else {
    layerControlObj.removeLayer(dataLayerObj);
    dataLayerObj = data_layer();
    dataLayerObj.setOpacity($('#opacity-slider').val());
    layerControlObj.addOverlay(dataLayerObj , "netcdf Layer");
  }
}

function get_files() {
  var url = $('#url-input').val();
  $.ajax({
    url: '/apps/netcdfviewer/files/',
    data: {'url': url,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var passedFiles = result['files'];
      var html = ''
      for (file in passedFiles) {
        html += '<div class="file" style="width: 100%; height: 30px;"><p style="padding: 5px 0px 5px 30px;">' + file + '</p></div>'
      }
      $('#filetree-div').empty();
      $('#filetree-div').append(html);
    }
  });
}



$('#url-input').change(function () {get_files();});
$('.file').click(function () {console.log('clicked')})

$('#wmslayer-style').change(function () {update_wmslayer();});
$('#wmslayer-bounds').change(function () {update_wmslayer();});
$('#opacity-slider').change(function () {dataLayerObj.setOpacity($('#opacity-slider').val())});

