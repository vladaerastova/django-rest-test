from django.db import models
from django.conf import settings

# Create your models here.


class Account(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	city = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	company_domain = models.CharField(max_length=255)
	company_name = models.CharField(max_length=255)
	role_in_company = models.CharField(max_length=255)
	title_in_company = models.CharField(max_length=255)
	linkedin = models.CharField(max_length=255)
