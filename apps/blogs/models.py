from django.db import models


class Source(models.Model):

    source_types = (('blogger', 'Blogger'),)
    type = models.CharField(max_length=50, choices=source_types)
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{0} on {1}'.format(self.username, self.get_type_display())


class Blog(models.Model):

    source = models.ForeignKey(Source, related_name='blogs')
    domain = models.CharField(max_length=255)
    default_domain = models.CharField(max_length=255)
    identificator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.domain or self.default_domain
