from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(author=self.id)
        post_rating = sum([r.post_rating * 3 for r in posts])
        comment_rating = sum([r.comment_rating for r in Comment.objects.filter(author=self.author)])
        sum_rating = sum([r.comment_raiting for r in Comment.objects.filter(post__in = posts)])
        self.author_rating = post_rating + comment_rating + sum_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'

    TYPE = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]

    type = models.CharField(max_length=2, choices=TYPE, default=NEWS)
    created_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', )
    header = models.CharField(max_length=255)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        preview = self.text[:124] + '...'
        return preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
