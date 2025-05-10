from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Commission(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Full", "Full"),
        ("Completed", "Completed"),
        ("Discontinued", "Discontinued"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='Open'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])
    
    def __str__(self):
        return self.title


class Job(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Full", "Full"),
    )
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        related_name='job'
    )
    role = models.TextField()
    manpower_required = models.IntegerField()
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='Open'
    )

    class Meta:
        ordering = ['status', '-manpower_required', 'role']

    
class JobApplication(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        related_name="application"
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']
