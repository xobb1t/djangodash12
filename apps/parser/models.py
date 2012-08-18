from django.db import models


class Process(models.Model):

    STAGE_CHOICES = (
        ('start', 'Start'),
        ('end', 'End'),
    )

    blog = models.OneToOneField('blogs.Blog')
    repo = models.OneToOneField('repositories.Repo')
    stage = models.CharField(max_length=255, choices=STAGE_CHOICES)
    error = models.TextField(blank=True)
    data = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{0} in {1}: {2}'.format(self.blog, self.repo,
            self.get_stage_display())
