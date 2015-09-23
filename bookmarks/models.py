from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    url = models.URLField(unique=True)
    def __str__(self):
        return self.url
    
class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(
        max_length=200,
        default='Description here')
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    def __str__(self):
        return '%s : %s' % (self.user.username, self.title)
    