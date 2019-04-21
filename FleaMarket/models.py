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
    text = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORIES,
                                default='abstract', blank=False)


