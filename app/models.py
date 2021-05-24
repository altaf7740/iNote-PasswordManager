from django.db import models

# Create your models here.
class Registration(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.email
    

class Credential(models.Model):
    website = models.CharField(max_length=512)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    userid = models.ForeignKey(Registration, on_delete=models.CASCADE)