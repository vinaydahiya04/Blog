from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length = 264)
    text = models.TextField()
    title = models.CharField(max_length = 264)
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approve_comments(self):
        return self.comment.filter(approved_comment  = True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk':self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name = 'comment')
    author = models.CharField(max_length = 264)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    approved_comment = models.BooleanField(default = False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def __str__(self):
        return self.text