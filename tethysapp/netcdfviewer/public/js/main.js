let firstlayeradded = false;
let files = [];
let wmsurl = '';
let odurl = '';
let shpfileAdded = false;

add_user_layers();

function get_metadata() {
  console.log('odurl: ' + odurl)
  $.ajax({
    url: '/apps/netcdfviewer/metadata/',
    data: {'odurl': odurl,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var variables = result['variables'];
      var attrs = result['attrs'];
      print_metadata(variables, attrs);
      update_wmslayer();
    }
  })
}

function update_wmslayer() {
  if (firstlayeradded == true) {
    layerControlObj.removeLayer(dataLayerObj);
  }
  dataLayerObj = data_layer();
  dataLayerObj.setOpacity($('#opacity-slider').val());
  layerControlObj.addOverlay(dataLayerObj, 'netcdf Layer');
}

function print_metadata(variables, attrs) {
  var html = '';
  var html2 = '';
  console.log(variables)
  for (let vars in variables) {
    if (variables[vars].substr(0, 4) !== 'time') {
      html += '<option>' + variables[vars] + '</option>';
    }
  }
  for (var att in attrs) {
    html2 += '<b style="padding-left: 40px">' + att + ':<b/><p style="padding-left: 40px">' + attrs[att] + '</p>';
  }
  $('#variable-input').empty();
  $('#variable-input').append(html);
  $('#metadata-div').empty();
  $('#metadata-div').append(html2);
}

function update_filepath() {
  var newURL = ''
  var cont = true;
  var href = $(this).attr('id');
  var currentURL = $('#url-input').val();
  var hrefArray = href.split('/')
  var currentArray = currentURL.split('/');

  if (currentURL !== files[files.length - 1]) {
    files.push(currentURL);
  }

  currentArray.forEach(function (val, index,) {
    hrefArray.forEach(function (val2, index2) {
      if (val == val2 && val == 'thredds' && cont == true) {
        for (var i = index; i <= currentArray.length; i++) {
          currentArray.pop();
        }
        for (var i = 0; i <= hrefArray.length - 1; i++) {
          currentArray.push(hrefArray[i]);
        }
        cont = false;
      }
    });
  });

  if (cont == true) {
    currentArray.pop();
    for (var i = 0; i <= hrefArray.length - 1; i++) {
      currentArray.push(hrefArray[i]);
    }
  }

  currentArray.forEach(function (value, i) {
    if (value == '' || value == undefined) {
      currentArray.splice(i, 1);
    }
    if (i == 0) {
      newURL = currentArray[i];
    } else if (i == 1) {
      newURL = newURL + '//' + currentArray[i];
    } else {
      newURL = newURL + '/' + currentArray[i];
    }
  })
  $('#url-input').val(newURL)
  get_files(newURL);
}

function get_files(url) {
  $.ajax({
    url: '/apps/netcdfviewer/files/',
    data: {'url': url,},
    dataType: 'json',
    contentType: "application/json",
    method: 'GET',
    success: function (result) {
      var passedFiles = result['files'];
      var folder = result['folder'];
      var correctURL = result['correct_url'];
      if (correctURL.substr(0, 4) == 'http') {
        $('#url-input').val(correctURL);
      }
      if (passedFiles == false) {
        $('#metadata-div').empty();
        $('#metadata-div').append('<p style="padding: 10px 0px 10px 40px">NO DATA!!!</p>');
      } else if (folder == true) {
        var html = ''
        if(passedFiles.length < 1 || passedFiles == undefined){
          html = '<div style="width: 100%; height: 30px;"><p>No Files Found!!!</p></div>'
        } else {
          for (var file in passedFiles) {
            html += '<div id="' + passedFiles[file] + '" class="file" style="width: 100%; height: 30px;" ' +
                'onclick="update_filepath.call(this)"><p>' + file + '</p></div>';
          }
        }
        $('#filetree-div').empty();
        $('#filetree-div').append(html);
      } else {
        var currentURL = $('#url-input').val();
        currentURL = currentURL.split('/thredds/')[0];
        wmsurl = currentURL + passedFiles['WMS:'];
        odurl = currentURL + passedFiles['OPENDAP:'];
        var newURL = files[files.length - 1]
        $('#url-input').val(newURL)
        get_files(newURL);
        files.pop();
        get_metadata();
      }
    }
  });
}

$('#up-file').click(function () {
  if (files.length !== 0) {
    var newURL = files[files.length - 1]
    $('#url-input').val(newURL);
    get_files(newURL);
    files.pop();
  }
})

$('#url-input').change(function () {get_files($('#url-input').val());});
$('#variable-input').change(function () {update_wmslayer();});
$('#wmslayer-style').change(function () {update_wmslayer();});
$('#wmslayer-bounds').change(function () {update_wmslayer();});
$('#opacity-slider').change(function () {dataLayerObj.setOpacity($('#opacity-slider').val())});
$('#upload-shp').click(function() {$('#uploadshp-modal').modal('show')});
