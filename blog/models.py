from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_articles'
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_articles'
    )
    entry = models.TextField()
    header_image = models.ImageField(upload_to='article_headers/', blank=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.pk])


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        author_name = self.author if self.author else "Unknown"
        return f'Comment by {author_name} on {self.article}'

class ArticleImage(models.Model):
    image = models.ImageField(upload_to='images/', null=True)
    caption = models.CharField(max_length=255, blank=True)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
