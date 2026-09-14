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


class Experience(models.Model):
    title = models.CharField(max_length=255)
    title_id = models.CharField(max_length=255, blank=True, default="")
    organization = models.CharField(max_length=255)
    organization_id = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField()
    description_id = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "main_portfolio_experience"

    @property
    def is_ongoing(self):
        return self.end_year is None

    def __str__(self):
        return self.title
