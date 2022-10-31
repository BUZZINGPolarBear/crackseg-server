from django.db import models

class FileUpload(models.Model):
    title = models.TextField(null=True)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title