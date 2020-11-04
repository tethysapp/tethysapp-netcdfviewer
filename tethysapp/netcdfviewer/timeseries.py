from django.http import JsonResponse
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

    #fix times
    time_dic = []

    ds = nc.Dataset(path_to_netcdf)
    units = ds[time].units
    times = ds[time][:]
    for time in times:
        ti = nc.num2date(time, units)
        time_dic.append(ti)

    ds.close()
    data['datetime'] = time_dic
    ##

    for t in enumerate(data.datetime):
        data.datetime[t[0]] = str(t[1])

    return JsonResponse({'data': data, 'time': datetime, 'value': value})


def inspect_netcdf(request):
    inspect = {}
    variable = {}
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    nc_obj = nc.Dataset(path_to_netcdf, 'r', clobber=False, diskless=True, persist=False)

    inspect['object'] = str(nc_obj)
    inspect['varLength'] = str(len(nc_obj.variables))
    inspect['dimLength'] = str(len(nc_obj.dimensions))
    inspect['globAtt'] = str(nc_obj.__dict__)

    for vars in nc_obj.variables.keys():
        variable['varName'] = str(vars)
        variable['varView'] = str(nc_obj[vars])
        variable['varData'] = str(nc_obj[vars][:])
        variable['varDims'] = str(nc_obj[vars].dimensions)
        variable['varMeta'] = str(nc_obj[vars].__dict__)
        inspect[str(vars)] = variable
        variable = {}

    for dims in nc_obj.dimensions.keys():
        inspect[str(dims)] = str(nc_obj.dimensions[dims].size)


    nc_obj.close()
    return JsonResponse({'inspect': inspect})
