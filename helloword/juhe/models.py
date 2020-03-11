from django.db import models


# Create your models here.

class User1(models.Model):
    openid = models.CharField(max_length=64, unique=True)
    nickname = models.CharField(max_length=64)
    focus_cities = models.TextField(default=[])
    focus_constructions = models.TextField(default=[])
    focus_stocks = models.TextField(default=[])
    # menu = models.ManyToManyField(App)

    def __str__(self):
        return self.nickname

    class Meta:
        indexes = [
            models.Index(fields=['nickname'], name='nickname')
        ]
