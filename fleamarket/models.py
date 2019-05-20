"""Ad model"""
import sys
from io import BytesIO
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from subscriptions.tasks import make_a_mailing
from .helpers import FileValidator, ImagePath


class AbstractAd(models.Model):
    """Simple ad model"""
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
                image = Image.open(self.image)
                if image.size != (468, 60):
                    output = BytesIO()
                    # Resize/modify the image
                    image = image.resize((300, 200))
                    # after modifications, save it to the output
                    image.save(output, format='png', quality=100)
                    output.seek(0)
                    # change the imagefield value to be the newley modifed image value
                    self.image = InMemoryUploadedFile(output, 'ImageField',
                                                      "%s.png" % self.image.name.split('.')[0],
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
        image_name = self.image.name
        # Delete the model before the file
        super().delete(*args, **kwargs)
        # Delete the file after the model
        if image_name:
            storage.delete(image_name)

    @property
    def get_header(self):
        if self.header is not None:
            return self.header

        return 'Ad #{}'.format(self.pk)


@receiver(post_save, sender=AbstractAd)
def ad_post_save_handler(sender, **kwargs):
    if not kwargs['created']:
        return

    make_a_mailing(kwargs['instance'])
