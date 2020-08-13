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
    description = ''
    tags = ''
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
        )

        return url_maps