let firstlayeradded = false;

function update_wmslayer() {
  if( !$('#server-input').val() || !$('#file-path-input').val() || !$('#variable-input').val()) {
    alert('Please provide the needed values.')
  } else {
    layerControlObj.removeLayer(dataLayerObj);
    dataLayerObj = data_layer();
    dataLayerObj.setOpacity($('#opacity-slider').val());
    layerControlObj.addOverlay(dataLayerObj , "netcdf Layer");
  }
}

function get_metadata() {
  let wmsurl = $('#server-input').val() + $('#file-path-input').val();
  let path = wmsurl.replace('wms', 'wcs');
  console.log(path);
/*  $.ajax({
    url: '/apps/dataviewer/options/file_tree/',
    data: {'url': wmsurl,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
    }
  })*/
}

$('#get-wmslayer').click(function () {update_wmslayer();});
$('#get-metadata').click(function () {get_metadata();});
$('#wmslayer-style').change(function () {update_wmslayer();});
$('#wmslayer-bounds').change(function () {update_wmslayer();});
$('#opacity-slider').change(function () {dataLayerObj.setOpacity($('#opacity-slider').val())});

