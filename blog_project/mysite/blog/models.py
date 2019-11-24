from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  #connected author to actual authorization user
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # after someone creates a post where should the website take them? : get_absolute_url tells that
    #the name should be this only as django looks for this name only, we cant call it something else
     # we are using DetailView
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)  #comments connected to a blog post
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    # after someone creates a post where should the website take them? : get_absolute_url tells that
    #the name should be this only as django looks for this name only, we cant call it something else
    # comment needs to be approved by superuser we redirect to list of all posts (homepage)
    # we use ListView
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
