import hashlib
import os

from datetime import datetime

from django.db import models
from django.conf import settings


class Process(models.Model):

    blog = models.OneToOneField('blogs.Blog')
    repo = models.OneToOneField('repositories.Repo')
    error = models.TextField(blank=True)
    stage = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=40)

    def __unicode__(self):
        return u'{0} in {1}: {2}%'.format(
            self.blog, self.repo, self.stage
        )

    def save(self, *args, **kwargs):
        if not self.hash:
            time = datetime.now().isoformat()
            salt = '{0}${1}${2}'.format(
                settings.SECRET_KEY,
                self.blog.domain,
                time
            )
            self.hash = hashlib.sha1(salt).hexdigest()
        super(Process, self).save(*args, **kwargs)

    @property
    def path(self):
        return os.path.join(settings.BLOGS_ROOT, self.hash)

    def update_stage(self, val):
        self.stage = val
        self.save()
