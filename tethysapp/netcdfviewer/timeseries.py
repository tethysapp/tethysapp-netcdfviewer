from django.http import JsonResponse
import xarray
import requests


def get_point_values(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    url = request.GET['odurl']
    var = request.GET['var']

    ds = xarray.open_dataset(url)
    time_series = ds[var].sel(latitude=lat, longitude=lon, method='nearest')
    yvals = time_series.values.tolist()
    xvals = time_series['time'].dt.strftime('%Y-%m-%dT%H:%M:%S').values.tolist()

    return JsonResponse({'x': xvals, 'y': yvals})


def get_box_values(request):
    maxlat = float(request.GET['maxlat'])
    maxlon = float(request.GET['maxlng'])
    minlat = float(request.GET['minlat'])
    minlon = float(request.GET['minlng'])
    url = request.GET['odurl']
    var = request.GET['var']

    ds = xarray.open_dataset(url)
    time_series = ds[var].sel(latitude=slice(maxlat, minlat), longitude=slice(maxlon, minlon)).mean(dim=['latitude', 'longitude'])

    yvals = time_series.values.tolist()
    xvals = time_series['time'].dt.strftime('%Y-%m-%dT%H:%M:%S').values.tolist()
    print(time_series)

    return JsonResponse({'x': xvals, 'y': yvals})
