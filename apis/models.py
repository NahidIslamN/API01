from django.db import models


from django.contrib.auth.models import User

# Create your models here.






class Products(models.Model):
    name = models.CharField(max_length=100)
    oner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    





