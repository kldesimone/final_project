from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import os
import uuid
def upload_to_location(instance, filename):
  blocks = filename.split('.')
  ext = blocks[-1]
  filename = "%s.%s" % (uuid.uuid4(), ext)
  instance.title = blocks[0]
  return os.path.join('uploads/', filename)

# Create your models here.
class Destination(models.Model):
  destination = models.CharField(max_length=300)
  point_of_interest = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return self.destination

  def get_absolute_url(self):
    return reverse("destination_detail", args=[self.id])

class Recommendation(models.Model):
  destination = models.ForeignKey(Destination)
  user = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)
  recommendation = models.TextField()
  location = models.CharField(default='', max_length=300)
  image_file= models.ImageField(upload_to=upload_to_location, null=True, blank=True)


  def __unicode__(self):
    return self.text

class Vote(models.Model):
  user = models.ForeignKey(User)
  recommendation =  models.ForeignKey(Recommendation, blank=True, null=True)

  def __unicode__(self):
    return "%s upvoted" % (self.user.username)