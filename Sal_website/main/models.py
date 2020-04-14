from django.db import models

# Create your models here.

class InfoPrompt(models.Model):
    org_name = models.CharField(max_length=200)
    org_email = models.CharField(max_length=200)
    # map_updated = models.DateTimeField("last updated")


    def __str__(self):
        return self.org_name

