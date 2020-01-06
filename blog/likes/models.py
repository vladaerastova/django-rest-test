from django.db import models
from django.conf import settings
from posts.models import Post

# Create your models here.


class Like(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return str(self.user.username)
