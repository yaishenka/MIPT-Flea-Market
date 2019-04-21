from django.db import models
from django.contrib.auth import get_user_model


class AbstractAd(models.Model):
    CATEGORIES = (
        ("abstract", 'Abstract'),
        ("cars", 'Cars'),
        ("appliances", 'Appliances'),
        ("gadgets", 'Gadgets'),
    )

    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    header = models.CharField(max_length=50, default=None, blank=True, null=True)
    text = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORIES,
                                default='abstract', blank=False)

    @property
    def get_header(self):
        if self.header is not None:
            return self.header
        else:
            return 'Ad #{}'.format(self.pk)



