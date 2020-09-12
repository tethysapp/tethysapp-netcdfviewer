let chartdata = {};

drawnItems.on('click', function (e) {
  get_coords(e);
});

/* Controls for when drawing on the maps */
mapObj.on(L.Draw.Event.CREATED, function (e) {
  drawnItems.addLayer(e.layer);
  get_coords(e);
});

shpLayer.on('click', function (e) {
  var layer = e.layer;
  var coords = layer.getBounds();
  console.log(coords);
  var type = 'rectangle';
  get_timeseries(type, coords);
});

function get_coords(e) {
  var layer = e.layer;
  if (layer instanceof L.Rectangle) {
    var type = 'rectangle';
    var coord = layer.getLatLngs();
    var coords = {'_southWest': {'lat': 0, 'lng': 0}, '_northEast': {'lat': 0, 'lng': 0}};
    console.log(coords);
    coords['_northEast'].lat = coord[0][2].lat;
    coords['_southWest'].lng = coord[0][0].lng;
    coords['_southWest'].lat = coord[0][0].lat;
    coords['_northEast'].lng = coord[0][2].lng;
  } else {
    var type = 'marker';
    var coords = layer.getLatLng();
  }
  get_timeseries(type, coords);
}

function get_timeseries(type, coords) {
  if (odurl == '') {
    alert('Please select a data layer.');
  } else {
    if (type === 'marker') {
      var coord = [];
      coord.push(coords.lat);
      coord.push(coords.lng);
      var maxlat = coord[0] + 0.5;
      var maxlng = coord[1] + 0.5;
      var minlat = coord[0] - 0.5;
      var minlng = coord[1] - 0.5;
    } else if (type === 'rectangle') {
      var coord = false;
      var maxlat = coords['_northEast'].lat;
      var maxlng = coords['_northEast'].lng;
      var minlat = coords['_southWest'].lat;
      var minlng = coords['_southWest'].lng;
    }

    var vars = $('#variable-input').val();
    $.ajax({
      url: 'timeseries/get_box_values/',
      data: {
        'maxlat': maxlat,
        'maxlng': maxlng,
        'minlat': minlat,
        'minlng': minlng,
        'coord': JSON.stringify(coord),
        'odurl': odurl,
        'var': vars,
      },
      dataType: 'json',
      contentType: "application/json",
      method: 'GET',
      success: function (result) {
        var data = result['data'];
        var time = result['time'];
        var value = result['value'];
        draw_graph(data, time, value);
        $('#timeseries-model').modal('show');
      },
    });
  }
}

function draw_graph(data, time, value) {
    var series = $.parseJSON(data);
    var length = Object.keys(series[time]).length;
    let x = [];
    let y = [];
    var i;
    for (i = 0; i < length; i++) {
        x.push(series[time][i]);
        y.push(series[value][i]);
    }

    console.log(x)
    console.log(y)

    let variable = $('#variable-input').val();
    let layout = {
        title: 'Mean of ' + variable,
        xaxis: {title: 'Time'},
        yaxis: {title: 'Amount (mm)'}
    };

    let values = {
        x: x,
        y: y,
        mode: 'lines+markers',
        type: 'scatter'
    };
    Plotly.newPlot('chart', [values], layout);
    let chart = $("#chart");
    chart.css('height', 500);
    Plotly.Plots.resize(chart[0]);
}

// Add function to save chart to CSV

function chartToCSV() {
  function zip(arrays) {
    return arrays[0].map(function (_, i) {
      return arrays.map(function (array) {
        return array[i]
      })
    });
  }
  if (chartdata === {}) {
    alert('There is no data in the chart. Please plot some data first.');
    return
  }
  let data = zip([chartdata.x, chartdata.y]);
  let csv = "data:text/csv;charset=utf-8," + data.map(e => e.join(",")).join("\n");
  let link = document.createElement('a');
  link.setAttribute('href', encodeURI(csv));
  link.setAttribute('target', '_blank');
  link.setAttribute('download', 'extracted_time_series.csv');
  document.body.appendChild(link);
  link.click();
  $("#a").remove()
}

// WHEN YOU CLICK ON THE DOWNLOAD BUTTON- RUN THE DOWNLOAD CSV FUNCTION
$("#download-csv").click(chartToCSV);