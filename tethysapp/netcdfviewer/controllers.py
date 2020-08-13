from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button, TextInput, SelectInput, RangeSlider

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )
    server_input = TextInput(display_text='Thredds server',
                             name='server-input',
                             initial='https://thredds.servirglobal.net',
                             )
    file_input = TextInput(display_text='WMS file path',
                           name='file-path-input',
                           initial='/thredds/wms/climateserv/'
                                   'ucsb-chirps-gefs/global/0.05deg/10dy/ucsb-chirps-gefs.daily.2020.nc4',
                           )
    variable_input = TextInput(display_text='Variable to display',
                               name='variable-input',
                               initial='precipitation_amount',
                               )
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
        'server_input': server_input,
        'file_input': file_input,
        'variable_input': variable_input,
        'layer_style': layer_style,
        'layer_range': layer_range,
        'save_button': save_button,
    }

    return render(request, 'netcdfviewer/home.html', context)
