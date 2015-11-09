from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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

  def __unicode__(self):
    return self.text