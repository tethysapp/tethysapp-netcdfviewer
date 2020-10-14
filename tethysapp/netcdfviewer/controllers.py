from django.http import JsonResponse
from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button, TextInput, SelectInput, RangeSlider
from siphon.catalog import TDSCatalog
import requests
import xarray as xr


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    layer_style = SelectInput(display_text='Select Color Style',
                              name='wmslayer-style',
                              multiple=False,
                              options=[('RAINBOW', 'boxfill/rainbow'), ('OCCAM', 'boxfill/occam'),
                                       ('ALG', 'boxfill/alg'), ('ALG2', 'boxfill/alg2'),
                                       ('GRAYSCALE', 'boxfill/greyscale'), ('SST_36', 'boxfill/sst_36'),
                                       ('NC VIEW', 'boxfill/ncview'), ('RED BLUE', 'boxfill/redblue')],
                              initial=['RAINBOW'],
                              )

    layer_range = TextInput(display_text='Set Data Bounds',
                            name='wmslayer-bounds',
                            initial='0,100',
                            )

    context = {
        'layer_style': layer_style,
        'layer_range': layer_range,
    }

    return render(request, 'netcdfviewer/home.html', context)


def build_data_tree(request):
    url = request.GET['url']
    ds = TDSCatalog(url)
    data_tree = {}
    folders_dict = {}
    files_dict = {}

    folders = ds.catalog_refs
    for x in enumerate(folders):
        folders_dict[folders[x[0]].title] = folders[x[0]].href

    files = ds.datasets
    for x in enumerate(files):
        files_dict[files[x[0]].name] = files[x[0]].access_urls

    data_tree['folders'] = folders_dict
    data_tree['files'] = files_dict
    correct_url = ds.catalog_url
    return JsonResponse({'dataTree': data_tree, 'correct_url': correct_url})


def metadata(request):
    url = request.GET['opendapURL']
    ds = xr.open_dataset(url)
    dimensions = ds.coords
    str_attrs = {}
    variables = {}
    var_attr = {}
    dims = []

    for dim in dimensions:
        dims.append(dim)

    for attr in ds.attrs:
        str_attrs[str(attr)] = str(ds.attrs[attr])

    for var in ds.data_vars:
        for attr in ds[var].attrs:
            var_attr[str(attr)] = str(ds[var].attrs[attr])

        variables[str(var)] = var_attr
        var_attr = {}

    return JsonResponse({'variables': variables, 'dims': dims, 'attrs': str_attrs})


def get_dimensions(request):
    url = request.GET['opendapURL']
    variable = request.GET['variable']
    ds = xr.open_dataset(url)
    dimensions = ds[variable].coords
    print(dimensions)
    return JsonResponse({'dims': dimensions})
