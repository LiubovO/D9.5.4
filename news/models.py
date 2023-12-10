from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        posts = Post.objects.filter(author=self)
        for p in posts:
            posts_rating += p.rating
        comments_rating = 0
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comments_rating += c.rating
        posts_comments_rating = 0
        posts_comments = Comment.objects.filter(post__author=self)
        for pc in posts_comments:
            posts_comments_rating += pc.rating
        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribe = models.ManyToManyField(User, through='CategorySubscribe')

    def __str__(self):
        return self.name.title()

class CategorySubscribe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subscriber = models.ForeignKey(User, on_delete=models.PROTECT)


class Post(models.Model):
    post = 'PST'
    news = 'NWS'

    TYPE = [
        (post, "Статья"),
        (news, "Новость")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=7, choices=TYPE, default='NWS')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_text = self.text[0:124] + '...'
        return small_text

    def __str__(self):
        return f'{self.title}/n {self.text}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'