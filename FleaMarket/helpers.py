from django.utils.deconstruct import deconstructible
import os
import uuid
from PIL import Image
from os.path import splitext
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

@deconstructible
class FileValidator(object):
    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    width_message = _(
        'The current image width %(width)s, which is not allowed. The allowed width  is %(allowed_width)s.')
    height_message = _(
        'The current image height %(height)s, which is not allowed. The allowed height  is %(allowed_height)s.')
    min_size_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = []
        self.allowed_extensions.extend(kwargs.pop('allowed_extensions', None))
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)
        self.allowed_width = kwargs.pop('allowed_width', None)
        self.allowed_height = kwargs.pop('allowed_height', None)

    def __call__(self, value):
        pass
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and not ext in self.allowed_extensions:
            message = self.extension_message % {
                'extension': ext,
                'allowed_extensions': self.allowed_extensions
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }

            raise ValidationError(message)
        try:
            # Check height and width
            image = Image.open(value)
            (width, height) = image.size
            if self.allowed_width and self.allowed_width != width:
                message = self.width_message % {
                    'width': width,
                    'allowed_width': self.allowed_width
                }
                raise ValidationError(message)

            if self.allowed_height and self.allowed_height != height:
                message = self.height_message % {
                    'height': height,
                    'allowed_width': self.allowed_height
                }
                raise ValidationError(message)
        except OSError:
            return


@deconstructible
class ImagePath(object):
    def __init__(self, path, width=0, height=0, extension=''):
        self.width = width
        self.height = height
        self.extension = extension
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        extension = os.path.splitext(filename)[1]
        imagePath = self.path % (uuid.uuid4(), extension)
        return imagePath