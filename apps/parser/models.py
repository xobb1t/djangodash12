import hashlib
import os

from django.db import models
from django.conf import settings


class Process(models.Model):

    STAGE_CHOICES = (
        ('start', 'Start'),
        ('end', 'End'),
    )

    blog = models.OneToOneField('blogs.Blog')
    repo = models.OneToOneField('repositories.Repo')
    stage = models.CharField(max_length=255, choices=STAGE_CHOICES)
    error = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=40)

    def __unicode__(self):
        return u'{0} in {1}: {2}'.format(self.blog, self.repo,
            self.get_stage_display())

    def save(self, *args, **kwargs):
        if not self.hash:
            time = datetime.now().isoformat()
            salt = '{0}${1}${2}${3}'.format(
                settings.SECRET_KEY,
                self.pk,
                self.blog.domain,
                time
            )
            self.hash = hashlib.sha1(salt).hexdigest()
        super(Process, self).save(*args, **kwargs)

    @property
    def path(self):
        return os.path.join(settings.BLOGS_ROOT, 'blogs', self.hash)
