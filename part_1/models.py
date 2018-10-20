from django.db import models

# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='documents/')

class AppKeys(models.Model):
	CustomerKey = models.CharField(max_length = 100, blank = False)
	CustomerSecretKey = models.CharField(max_length = 100, blank = False)
	AccessTokenKey = models.CharField(max_length = 100, blank = False)
	AccessTokenSecret = models.CharField(max_length = 100, blank = False)

	def __str__(self):
		return str(self.CustomerKey)