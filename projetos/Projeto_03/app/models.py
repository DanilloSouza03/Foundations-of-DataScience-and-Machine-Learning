from django.db import models

# Create your models here.
class Products(models.Model):
    user_id = models.IntegerField()
    product = models.CharField(max_length=150)
    categoria = models.CharField(max_length=150)
    ratings = models.IntegerField()