from django.http import JsonResponse
from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button, TextInput, SelectInput, RangeSlider
import xarray as xr
import requests
from bs4 import BeautifulSoup


@login_required()
def home(request):
    """
    Controller for the app home page.

    server_input = TextInput(display_text='Thredds server',
                             name='server-input',
                             initial='https://thredds.servirglobal.net',
                             )
    file_input = TextInput(display_text='WMS file path',
                           name='file-path-input',
                           initial='/thredds/wms/climateserv/ucsb-chirps/global'
                                   '/0.05deg/daily/ucsb-chirps.daily.2020.nc4',
                           )
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

    od_url = 'https://thredds.servirglobal.net/thredds/dodsC/climateserv/ucsb-chirps-gefs' \
             '/global/0.05deg/10dy/ucsb-chirps-gefs.daily.2020.nc4'
    ds = xr.open_dataset(od_url)

    variables = []

    for var in ds.data_vars:
        variables.append(var)

    context = {
        #'server_input': server_input,
        #'file_input': file_input,
        'layer_style': layer_style,
        'layer_range': layer_range,
        'variables': variables,
    }

    return render(request, 'netcdfviewer/home.html', context)


def files(request):
    url = request.GET['url']
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text)
    files = {}

    for link in soup.find_all('a'):
        if hasattr(link.tt, 'text'):
            files[link.tt.text] = link.get('href')

    print(files)
    return JsonResponse({'url': url, 'files': files})
