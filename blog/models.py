from django.db import models
from django.conf import settings
from user_management.models import Profile
from django.urls import reverse

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Category' 
        verbose_name_plural = 'Categories'  # so that it's not written as "categorys" lmao

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True)
    entry = models.TextField()
    header_image = models.ImageField(upload_to='article_headers/')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="blog_comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'
