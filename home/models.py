from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    info = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    # profile = models.ImageField(upload_to='profile-images/%y/%m/%d/', default='profile-images/default/memerrank-no-dp.jpg', blank=False, null=False)
    

    def __str__(self):
        return self.title
