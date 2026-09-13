from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    title_id = models.CharField(max_length=255, blank=True, default="")
    description_id = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100)
    project_url = models.URLField(blank=True)
    thumbnail = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
