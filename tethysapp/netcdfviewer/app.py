from tethys_sdk.base import TethysAppBase, url_map_maker


class Netcdfviewer(TethysAppBase):
    """
    Tethys app class for NetCDF Viewer.
    """

    name = 'NetCDF Viewer'
    index = 'netcdfviewer:home'
    icon = 'netcdfviewer/images/nc.png'
    package = 'netcdfviewer'
    root_url = 'netcdfviewer'
    color = '#1600F0'
    description = 'An app for viewing files on a Thredds Data Serrver'
    tags = 'netCDF4, CHIRPS,'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='netcdfviewer',
                controller='netcdfviewer.controllers.home'
            ),
            UrlMap(
                name='files',
                url='netcdfviewer/files',
                controller='netcdfviewer.controllers.files'
            ),
            UrlMap(
                name='metadata',
                url='netcdfviewer/metadata',
                controller='netcdfviewer.controllers.metadata'
            ),
            UrlMap(
                name='uploadShapefile',
                url='netcdfviewer/shapefile/uploadShapefile/',
                controller='netcdfviewer.shapefile.uploadShapefile'
            ),
            UrlMap(
                name='user_geojson',
                url='netcdfviewer/shapefile/user_geojsons/',
                controller='netcdfviewer.shapefile.user_geojsons'
            ),
            UrlMap(
                name='get_box_values',
                url='netcdfviewer/timeseries/get_box_values/',
                controller='netcdfviewer.timeseries.get_box_values'
            ),
        )

        return url_maps
