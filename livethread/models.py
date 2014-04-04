from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class ThreadSpace(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse('thread', args=[str(self.id)])

    def __unicode__(self):
        return self.name

class ThreadMessage(models.Model):
    thread = models.ForeignKey(ThreadSpace)
    user = models.ForeignKey(User)
    text = models.TextField()




