from django.db import models

class User(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_left = models.IntegerField(default=0)
    connected = models.BooleanField(default=False)
    detail = models.CharField(max_length=100, default="")
    time = models.IntegerField(default=0)
    day =  models.CharField(max_length=15, default='Monday')

    def __str__(self):
        return self.detail

    def setDetail(self, detail_text):
    	self.detail = detail_text

    def set_time_left(self, time):
    	self.time_left = time

    def set_connected(self, boolean_in):
    	self.connected = boolean_in

    def max_time(self):
    	return int(self.time) + int(self.time_left)

