from django.http import JsonResponse
from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button, TextInput, SelectInput, RangeSlider
from bs4 import BeautifulSoup
from siphon.catalog import TDSCatalog
import xarray as xr
import requests


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


def files(request):
    url = request.GET['url']
    ds = TDSCatalog(url)
    folders_dict = {}

    folders = ds.catalog_refs
    for x in enumerate(folders):
        folders_dict[folders[x[0]].title] = folders[x[0]].href

    files = ds.datasets
    for x in enumerate(files):
        folders_dict[files[x[0]].title] = files[x[0]].access_urls

    files = False
    correct_url = ds.catalog_url
    return JsonResponse({'folder': folders_dict, 'files': files, 'correct_url': correct_url})



