from django.db import models


class User(models.Model):

    identification = models.CharField(max_length=16)
    username = models.CharField(max_length=40)
    access_token = models.CharField(max_length=255)

    def __unicode__(self):
        return self.username


class Repo(models.Model):

    user = models.ForeignKey('repositories.User', related_name='repos')
    blog = models.ForeignKey('blogs.Blog', related_name='repos', null=True)
    name = models.CharField(max_length=100)
    cname = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
