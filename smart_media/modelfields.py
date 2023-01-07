from django.conf import settings
from django.db import models

from .fields import SmartMediaField as SmartMediaFormField
from .validators import SmartMediaFileExtensionValidator


class SmartMediaField(models.FileField):
    """
    TODO:

    This should include default validators on extension and if possible the upload_to()
    with the field name
    """
    default_validators = [
        SmartMediaFileExtensionValidator(),
    ]

    #def generate_filename(self, instance, filename):
        #"""
        #Apply (if callable) or prepend (if a string) upload_to to the filename,
        #then delegate further processing of the name to the storage backend.
        #Until the storage layer, all file paths are expected to be Unix style
        #(with forward slashes).
        #"""
        #if callable(self.upload_to):
            #filename = self.upload_to(instance, filename)
        #else:
            #dirname = datetime.datetime.now().strftime(str(self.upload_to))
            #filename = posixpath.join(dirname, filename)
        #filename = validate_file_name(filename, allow_relative_path=True)
        #return self.storage.generate_filename(filename)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": SmartMediaFormField,
                **kwargs,
            }
        )
