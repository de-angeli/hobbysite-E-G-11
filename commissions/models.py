from django.db import models
from django.urls import reverse

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(null=False)
    updated_on = models.DateTimeField(null=False)

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

class Comment(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        related_name="comment"
    )
    entry = models.TextField()
    created_on = models.DateTimeField(null=False)
    updated_on = models.DateTimeField(null=False)

    class Meta:
        ordering = ['-created_on']

