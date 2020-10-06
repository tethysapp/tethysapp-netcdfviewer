from django.http import JsonResponse
import xarray
import geomatics
import json
import requests
import os
import urllib


def get_box_values(request):
    maxlat = float(request.GET['maxlat'])
    maxlon = float(request.GET['maxlng'])
    minlat = float(request.GET['minlat'])
    minlon = float(request.GET['minlng'])
    lat = request.GET['lat']
    lon = request.GET['lon']
    time = request.GET['time']
    url = request.GET['odurl']
    subset_url = request.GET['subsetURL']
    var = request.GET['var']
    coord = json.loads(request.GET['coord'])
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')

    print(coord)
    #try:
    print(json.loads(subset_url))
    urllib.request.urlretrieve(json.loads(subset_url), path_to_netcdf)
    #except:
    #    print('except!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #    var_dict = {lat: slice(maxlat, minlat), lon: slice(minlon, maxlon)}
    #    ds = xarray.open_dataset(url)
    #    time_series = ds[var].sel(var_dict)
    #    time_series.to_netcdf(path=path_to_netcdf)

    if coord is not False:
        data = geomatics.timeseries.point([path_to_netcdf], var, (coord[0], coord[1]), (lat, lon), time)
        datetime = 'datetime'
        value = 'values'
    else:
        data = geomatics.timeseries.full_array_stats([path_to_netcdf], var, time)
        datetime = 'datetime'
        value = 'mean'

    ds = xarray.open_dataset(path_to_netcdf)
    times = ds.coords['time']
    data['datetime'] = times

    for t in enumerate(data.datetime):
        data.datetime[t[0]] = str(t[1])

    print(data)
    return JsonResponse({'data': data, 'time': datetime, 'value': value})
