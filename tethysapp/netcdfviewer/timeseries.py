from django.http import JsonResponse
import xarray
import geomatics
import json
import requests
import os
import urllib
import netCDF4 as nc


def get_box_values(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    time = request.GET['time']
    subset_url = request.GET['subsetURL']
    var = request.GET['var']
    coord = json.loads(request.GET['coord'])
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    print(subset_url)

    urllib.request.urlretrieve(json.loads(subset_url), path_to_netcdf)

    if coord is not False:
        data = geomatics.timeseries.point([path_to_netcdf], var, (coord[0], coord[1]), (lat, lon), time)
        datetime = 'datetime'
        value = 'values'
    else:
        data = geomatics.timeseries.full_array_stats([path_to_netcdf], var, time)
        datetime = 'datetime'
        value = 'mean'

    ds = xarray.open_dataset(path_to_netcdf)
    times = ds.coords[time]
    data['datetime'] = times

    for t in enumerate(data.datetime):
        data.datetime[t[0]] = str(t[1])

    return JsonResponse({'data': data, 'time': datetime, 'value': value})


def inspect_netcdf(request):
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    nc_obj = nc.Dataset(path_to_netcdf, 'r', clobber=False, diskless=True, persist=False)

    inspect = "This is your netCDF python object \n" + str(nc_obj) + "\n\n " \
                "There are " + str(len(nc_obj.variables)) + " variables \n " \
                "There are " + str(len(nc_obj.dimensions)) + " dimensions \n\n " \
                "These are the global attributes of the netcdf file \n" + str(nc_obj.__dict__) + "\n\n" \
                "Detailed view of each variable"

    for variable in nc_obj.variables.keys():
        inspect += "Variable Name:  " + str(variable) + "\nThe view of this variable in the netCDF python object\n"\
                   + str(nc_obj[variable]) + "\nThe data array stored in this variable\n"\
                   + str(nc_obj[variable][:]) + "\nThe dimensions associated with this variable\n"\
                   + str(nc_obj[variable].dimensions) + "\nThe metadata associated with this variable\n"\
                   + str(nc_obj[variable].__dict__)

    for dimension in nc_obj.dimensions.keys():
        inspect += str(nc_obj.dimensions[dimension].size)

    nc_obj.close()
    print(inspect)
    return JsonResponse({'inspect': inspect})
