from datetime import datetime
from django.db import models


SOURCES = (('blogger', 'Blogger'),)


class SourceManager(models.Manager):

    def create_or_update(self, **kwargs):
        instance, created = self.get_or_create(**kwargs)
        defaults = kwargs.get('defaults', {})
        if not created:
            for key, value in defaults.items():
                setattr(instance, key, value)
            instance.save()
        return instance, created


class Source(models.Model):

    type = models.CharField(max_length=50, choices=SOURCES, default='blogger')
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    access_token = models.CharField(max_length=255)
    expiration_datetime = models.DateTimeField()

    objects = SourceManager()

    def __unicode__(self):
        return u'{0} on {1}'.format(self.username, self.get_type_display())

    @property
    def is_expired(self):
        return self.expiration_datetime < datetime.now()


class Blog(models.Model):

    source = models.ForeignKey(Source, related_name='blogs')
    domain = models.CharField(max_length=255)
    default_domain = models.CharField(max_length=255)
    identificator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.domain or self.default_domain
