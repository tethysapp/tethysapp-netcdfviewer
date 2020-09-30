from django.http import JsonResponse
import xarray
import geomatics
import json
import requests
import os


def get_box_values(request):
    maxlat = float(request.GET['maxlat'])
    maxlon = float(request.GET['maxlng'])
    minlat = float(request.GET['minlat'])
    minlon = float(request.GET['minlng'])
    lat = request.GET['lat']
    lon = request.GET['lon']
    time = request.GET['time']
    url = request.GET['odurl']
    var = request.GET['var']
    coord = json.loads(request.GET['coord'])
    var_dict = {lat: slice(maxlat, minlat), lon: slice(minlon, maxlon)}

    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    ds = xarray.open_dataset(url)

    time_series = ds[var].sel(var_dict)
    time_series.to_netcdf(path=path_to_netcdf)

    if not coord is False:
        data = geomatics.timeseries.point([path_to_netcdf], var, (coord[0], coord[1]), (lat, lon), time)
        time = 'datetime'
        value = 'values'
    else:
        data = geomatics.timeseries.full_array_stats([path_to_netcdf], var, time)
        time = 'datetime'
        value = 'mean'

    return JsonResponse({'data': data, 'time': time, 'value': value})
