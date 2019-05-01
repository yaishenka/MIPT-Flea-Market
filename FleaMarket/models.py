from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .helpers import FileValidator, ImagePath
from subscriptions.tasks import make_a_mailing
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.dispatch import receiver


class AbstractAd(models.Model):
    CATEGORIES = (
        ("abstract", 'Abstract'),
        ("cars", 'Cars'),
        ("appliances", 'Appliances'),
        ("gadgets", 'Gadgets'),
    )

    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    header = models.CharField(max_length=50, default=None, blank=True,
                              null=True)
    text = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORIES,
                                default='abstract', blank=False)
    image = models.ImageField(
        validators=[FileValidator(allowed_extensions=['png'])],
        upload_to=ImagePath('ads_images'),
        blank=True, null=True, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_image = self.image

    def save(self, *args, **kwargs):
        if self.image:
            try:
                # Opening the uploaded image
                im = Image.open(self.image)
                if im.size != (468, 60):
                    output = BytesIO()
                    # Resize/modify the image
                    im = im.resize((300, 200))
                    # after modifications, save it to the output
                    im.save(output, format='png', quality=100)
                    output.seek(0)
                    # change the imagefield value to be the newley modifed image value
                    self.image = InMemoryUploadedFile(output, 'ImageField',
                                                      "%s.png" %
                                                      self.image.name.split(
                                                          '.')[0],
                                                      'image/png',
                                                      sys.getsizeof(output),
                                                      None)
            except OSError:
                pass
            if self.old_image and self.image != self.old_image:
                try:
                    storage = self.old_image.storage
                    storage.delete(self.old_image.name)
                    self.old_image = self.image
                except:
                    pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage = self.image.storage
        imageName = self.image.name
        # Delete the model before the file
        super().delete(*args, **kwargs)
        # Delete the file after the model
        if (imageName):
            storage.delete(imageName)

    @property
    def get_header(self):
        if self.header is not None:
            return self.header
        else:
            return 'Ad #{}'.format(self.pk)

@receiver(post_save, sender=AbstractAd)
def ad_post_save_handler(sender, **kwargs):
    if not kwargs['created']:
        return

    make_a_mailing(kwargs['instance'])


