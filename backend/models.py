from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
	id = models.IntegerField(primary_key=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, blank=False)
	text = models.TextField(blank=False)
	favourite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)