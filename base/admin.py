import os
import zipfile
import StringIO

from django.conf import settings
from django.http import HttpResponse


class PrettyFilterMixin(object):

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"


class MediaRemovalAdminMixin(object):
    """
    This mixin overrides default delete_selected Admin action and replaces it
    with one that actually constructs a model instance from each object in the
    queryset and calls .delete() upon that instance.

    This way, we ensure that overridden delete method by MediaRemovalMixin
    is called.
    """

    def get_actions(self, request):
        actions = super(MediaRemovalAdminMixin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        # Add new delete method only for the superuser, as it is quite dangerous
        if request.user.is_superuser:

            # We use self.__class__ here so that self is not binded, otherwise
            # we would be passing 4 arguments instead of 3 (and self twice)
            new_delete = (self.__class__.delete_selected_with_media,
                          "delete_selected_with_media",
                          "Delete objects with associated media files")

            actions['delete_selected_with_media'] = new_delete

        return actions

    def delete_selected_with_media(self, request, queryset):
        for obj in queryset.all():
            obj.delete()


class DownloadMediaFilesMixin(object):

    def get_actions(self, request):
        actions = super(DownloadMediaFilesMixin, self).get_actions(request)

        # We use self.__class__ here so that self is not binded, otherwise
        # we would be passing 4 arguments instead of 3 (and self twice)
        export = (self.__class__.download_media_files,
                  "download_media_files",
                  "Download associated media files")

        actions['download_media_files'] = export
        return actions

    def download_media_files(self, request, queryset):
        export_file = 'export.zip'

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for obj in queryset.all():
            for filepath in obj.get_media_files():
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)

                if os.path.exists(filepath):
                    fdir, fname = os.path.split(filepath)
                    zf.write(filepath, fname)
                else:
                    self.message_user(request, '%s has no file saved at %s' %
                                                (obj, filepath))

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        response = HttpResponse(s.getvalue(),
                                mimetype="application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = (
            'attachment; filename=%s' % export_file
            )

        return response
