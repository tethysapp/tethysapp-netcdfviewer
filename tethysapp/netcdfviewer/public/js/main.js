let firstlayeradded = false;
let URLpath = [];
let subsetURL = '';
let wmsURL = '';
let opendapURL = '';
let shpfileAdded = false;

add_user_layers();

function update_filepath() {
  if ($(this).attr('class') == 'folder') {
    let newURL = $(this).attr('data-url');
    $('#url-input').val(newURL);
    get_files(newURL);
  } else if ($(this).attr('class') == 'file') {
    wmsURL = $(this).attr('data-wms-url');
    opendapURL = $(this).attr('data-opendap-url');
    subsetURL = $(this).attr('data-subset-url');
    get_metadata();
  }
}

function get_metadata() {
  $.ajax({
    url: '/apps/netcdfviewer/metadata/',
    data: {'opendapURL': opendapURL,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var variables = result['variables'];
      var attrs = result['attrs'];
      var dims = result['dims'];
      print_metadata(variables, attrs, dims);
      update_wmslayer();
    }
  })
}

function update_wmslayer() {
  if (firstlayeradded == true) {
    layerControlObj.removeLayer(dataLayerObj);
    mapObj.removeLayer(dataLayerObj);
  }
  dataLayerObj = data_layer();
  dataLayerObj.setOpacity($('#opacity-slider').val());
  layerControlObj.addOverlay(dataLayerObj, 'netcdf Layer');
}

function print_metadata(variables, attrs, dims) {
  var html = '';
  var html2 = '';
  var html3 = '';
  var html4 = '';
  for (let vars in variables) {
    html += '<option>' + vars + '</option>';
  }
  for (var i = 0; i < dims.length; i++) {
    html2 += '<option>' + dims[i] + '</option>';
  }
  for (var att in attrs) {
    html3 += '<b style="padding-left: 40px">' + att + ':<b/><p style="padding-left: 40px">' + attrs[att] + '</p>';
  }
  for (var varb in variables) {
    html4 += '<b style="padding-left: 40px">' + varb + ':<b/>'
    for (var attr in variables[varb]) {
      html4 += '<p style="padding-left: 40px">' + attr + ': ' + variables[varb][attr] + '</p>';
    }
  }
  $('#variable-input').empty();
  $('#variable-input').append(html);
  $('#variable-input option:nth-child(2)').attr('selected', 'selected');
  $('#time').empty();
  $('#time').append(html2);
  $('#lat').empty();
  $('#lat').append(html2);
  $('#lat option:nth-child(2)').attr('selected', 'selected');
  $('#lng').empty();
  $('#lng').append(html2);
  $('#lng option:nth-child(3)').attr('selected', 'selected');
  $('#metadata-div').empty();
  $('#metadata-div').append(html3);
  $('#var-metadata-div').empty();
  $('#var-metadata-div').append(html4);
  $('#file-metadata-button').css('background-color', 'rgba(205, 209, 253, 1)');
}

function get_files(url) {
  $.ajax({
    url: '/apps/netcdfviewer/buildDataTree/',
    data: {'url': url,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var dataTree = result['dataTree'];
      var correctURL = result['correct_url'];
      let html = ''
      for (var folder in dataTree['folders']) {
        html += '<div data-url="' + dataTree['folders'][folder] + '" class="folder" ' +
            'style="width: 100%; height: 30px; overflow-y: hidden" ' +
            'onclick="update_filepath.call(this)">' +
            '<p class="fas" style="display: inline-block">&#xf07b; ' + folder + '</p></div>'
      }
      for (var file in dataTree['files']) {
        html += '<div data-wms-url="' + dataTree['files'][file]['WMS'] + '' +
            '" data-subset-url="' + dataTree['files'][file]['NetcdfSubset'] + '' +
            '" data-opendap-url="' + dataTree['files'][file]['OPENDAP'] + '' +
            '" class="file" style="width: 100%; height: 30px;" ' +
            'onclick="update_filepath.call(this)"><p class="far" style="display: inline-block">' +
            '&#xf1c5; ' + file + '</p></div>';
      }
      $('#filetree-div').empty();
      $('#filetree-div').append(html);
      $('#url-input').val(correctURL);
      if (URLpath[URLpath.length - 1] !== correctURL) {
        URLpath.push(correctURL);
      }
    }
  });
}

function inspectNCDF() {
  $.ajax({
    url: '/apps/netcdfviewer/timeseries/inspect_netcdf',
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var inspect = result['inspect'];
      console.log(inspect)
      $('#inspect-div').append(inspect);
      $('#inspect-netcdf-model').modal('show');
    }
  });
}

function getDimensions() {
  let variable = $('#variable-input').val();
  console.log(variable);
  $.ajax({
    url: '/apps/netcdfviewer/getDimensions/',
    data: {
      'variable': variable,
      'opendapURL': opendapURL,
    },
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      let dims = result['dims'];
      let html = ''
      console.log(dims)
      for (var i = 0; i < dims.length; i++) {
        html += '<option>' + dims[i] + '</option>';
      }
      console.log('html: ' + html)
      $('#time').empty();
      $('#time').append(html2);
      $('#lat').empty();
      $('#lat').append(html2);
      $('#lat option:nth-child(2)').attr('selected', 'selected');
      $('#lng').empty();
      $('#lng').append(html2);
      $('#lng option:nth-child(3)').attr('selected', 'selected');
    }
  });
}

$('#up-file').click(function () {
  if (URLpath.length !== 1) {
    let newURL = URLpath[URLpath.length - 2]
    $('#url-input').val(newURL);
    get_files(newURL);
    URLpath.pop();
  }
})

$('#url-input').change(function () {get_files($('#url-input').val());});
$('#variable-input').change(function () {update_wmslayer();});
$('#wmslayer-style').change(function () {update_wmslayer();});
$('#wmslayer-bounds').change(function () {update_wmslayer();});
$('#opacity-slider').change(function () {dataLayerObj.setOpacity($('#opacity-slider').val())});
$('#variable-input').change(function () {getDimensions();});
$('#upload-shp').click(function() {$('#uploadshp-modal').modal('show')});
$('#inspect-netcdf').click(function () {inspectNCDF();});
$('#file-metadata-button').click(function() {
  $('#var-metadata-div').css('display', 'none');
  $('#metadata-div').css('display', 'block');
  $('#file-metadata-button').css('background-color', 'rgba(205, 209, 253, 1)');
  $('#var-metadata-button').css('background-color', 'rgba(130, 141, 205, 1)');
});
$('#var-metadata-button').click(function() {
  $('#metadata-div').css('display', 'none');
  $('#var-metadata-div').css('display', 'block');
  $('#var-metadata-button').css('background-color', 'rgba(205, 209, 253, 1)');
  $('#file-metadata-button').css('background-color', 'rgba(130, 141, 205, 1)');
});

