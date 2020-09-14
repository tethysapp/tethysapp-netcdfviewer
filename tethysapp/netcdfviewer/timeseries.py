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
    coord = json.loads(request.GET['coord'])
    url = request.GET['odurl']
    var = request.GET['var']
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    ds = xarray.open_dataset(url)

    time_series = ds[var].sel(latitude=slice(maxlat, minlat), longitude=slice(minlon, maxlon))
    time_series.to_netcdf(path=path_to_netcdf)

    if not coord is False:
        print('if')
        data = geomatics.timeseries.point([path_to_netcdf], var, (coord[0], coord[1]), dims=('latitude', 'longitude'), t_var='time')
        time = 'datetime'
        value = 'values'
    else:
        print('then')
        data = geomatics.timeseries.full_array_stats([path_to_netcdf], var, t_var='time')
        time = 'datetime'
        value = 'mean'


    return JsonResponse({'data': data, 'time': time, 'value': value})
