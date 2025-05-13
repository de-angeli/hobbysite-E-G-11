from django.db import models
from django.urls import reverse
from user_management.models import Profile


class Commission(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Full", "Full"),
        ("Completed", "Completed"),
        ("Discontinued", "Discontinued"),
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.TextField()
    status = models.CharField(
        max_length=20,
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
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    class Meta:
        ordering = ['status', '-manpower_required', 'role']

    def __str__(self):
        return self.role

    
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
        related_name="applications"
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return f"{self.applicant} applied to {self.job}"
