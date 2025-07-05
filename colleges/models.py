from django.db import models

# Create your models here.

class EnggCollegeInfo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name