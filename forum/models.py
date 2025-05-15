from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Thread Category"
        verbose_name_plural = "Thread Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ThreadCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='threads'
    )
    entry = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    
    def get_absolute_url(self):
        return reverse('forum:thread-detail', args=[self.pk])

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]
    
    def get_absolute_url(self):
        return reverse('forum:thread-detail', args=[self.thread.pk])

    def __str__(self):
        return f"Comment by {self.author or 'Anonymous'}"
