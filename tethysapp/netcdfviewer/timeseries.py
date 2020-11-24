from django.http import JsonResponse
#import geomatics
import json
import requests
import os
import urllib
import netCDF4 as nc
import numpy as np
import pandas as pd

ALL_STATS = ('mean', 'median', 'max', 'min', 'sum', 'std')
#############################Modified geomatics package##############################
def full_array_stats(files: list, var: str or int, t_var: str = 'time', fill_value: int = -9999, stats: list or str = 'mean'):

    stats = _gen_stat_list(stats)
    results = dict(datetime=[])
    for stat in stats:
        results[stat] = []

    for file in files:
        opened_file = nc.Dataset(file, 'r')
        results['datetime'] += list(_timesteps(opened_file, t_var))

        vs = opened_file[var][:]
        vs[vs == fill_value] = np.nan
        for stat in stats:
            results[stat] += _array_to_stat_list(vs, stat)

    return pd.DataFrame(results)


def _gen_stat_list(stats: str or list):
    if isinstance(stats, str):
        if stats == 'all':
            return ALL_STATS
        else:
            return stats.lower().replace(' ', '').split(',')
    if any(stat not in ALL_STATS for stat in stats):
        raise ValueError(f'Unrecognized stat requested. Choose from: {ALL_STATS}')


def _timesteps(file: str, time_dim):
    time_list = []
    units = file[time_dim].units
    times = file[time_dim][:]

    for ti in times:
        time_list.append(nc.num2date(ti, units))

    return time_list


def _array_to_stat_list(array: np.array, statistic: str):
    list_of_stats = []
    # add the results to the lists of values and times
    if array.ndim == 1 or array.ndim == 2:
        if statistic == 'mean':
            list_of_stats.append(np.nanmean(array))
        elif statistic == 'median':
            list_of_stats.append(np.nanmedian(array))
        elif statistic == 'max':
            list_of_stats.append(np.nanmax(array))
        elif statistic == 'min':
            list_of_stats.append(np.nanmin(array))
        elif statistic == 'sum':
            list_of_stats.append(np.nansum(array))
        elif statistic == 'std':
            list_of_stats.append(np.nanstd(array))
        elif '%' in statistic:
            list_of_stats.append(np.nanpercentile(array, int(statistic.replace('%', ''))))
        else:
            raise ValueError(f'Unrecognized statistic, {statistic}. Use stat_type= mean, min or max')
    elif array.ndim > 2:
        for v in array:
            list_of_stats += _array_to_stat_list(v, statistic)
    else:
        raise ValueError('Too many dimensions in the array. You probably did not mean to do stats like this')
    return list_of_stats

###########################################################################################

def get_box_values(request):
    time = request.GET['time']
    subset_url = request.GET['subsetURL']
    var = request.GET['var']
    path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
    try:
        urllib.request.urlretrieve(json.loads(subset_url), path_to_netcdf)
    except RuntimeError:
        return JsonResponse({'data': 'Invalid file'})

    try:
        #data = geomatics.timeseries.full_array_stats([path_to_netcdf], var, time)
        data = full_array_stats([path_to_netcdf], var, time)
    except RuntimeError:
        return JsonResponse({'data': 'Invalid dimensions'})
    datetime = 'datetime'
    value = 'mean'

#    time_dic = []

#    ds = nc.Dataset(path_to_netcdf)
#    units = ds[time].units
#    times = ds[time][:]
#    for time in times:
#        ti = nc.num2date(time, units)
#        time_dic.append(ti)

#    ds.close()
#    data['datetime'] = time_dic

    for t in enumerate(data.datetime):
        data.datetime[t[0]] = str(t[1])

    print(data)
    print(datetime)

    return JsonResponse({'data': data, 'time': datetime, 'value': value})


# def inspect_netcdf(request):
#     inspect = {}
#     variable = {}
#     path_to_netcdf = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'temp.nc')
#     nc_obj = nc.Dataset(path_to_netcdf, 'r', clobber=False, diskless=True, persist=False)
#
#     inspect['object'] = str(nc_obj)
#     inspect['varLength'] = str(len(nc_obj.variables))
#     inspect['dimLength'] = str(len(nc_obj.dimensions))
#     inspect['globAtt'] = str(nc_obj.__dict__)
#
#     for vars in nc_obj.variables.keys():
#         variable['varName'] = str(vars)
#         variable['varView'] = str(nc_obj[vars])
#         variable['varData'] = str(nc_obj[vars][:])
#         variable['varDims'] = str(nc_obj[vars].dimensions)
#         variable['varMeta'] = str(nc_obj[vars].__dict__)
#         inspect[str(vars)] = variable
#         variable = {}
#
#     for dims in nc_obj.dimensions.keys():
#         inspect[str(dims)] = str(nc_obj.dimensions[dims].size)
#
#
#     nc_obj.close()
#     return JsonResponse({'inspect': inspect})
