from django.db import models

class User(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	detail = models.CharField(max_length=100)
	time = models.IntegerField(default=0)
	day =  models.CharField(max_length=15, default='Monday')

	def __str__(self):
		return self.detail
