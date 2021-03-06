from django.core.files.storage import FileSystemStorage


class OverwriteFileSystemStorage(FileSystemStorage):
    """
    Rewrites the file instead of appending the _1, _2 prefix.
    """

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteFileSystemStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

