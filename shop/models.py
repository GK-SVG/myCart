from django.db import models

# Create your models here.


class Product(models.Model):
    pro_id = models.AutoField
    pro_name = models.CharField(max_length=50)
    pro_desc = models.CharField(max_length=300)
    categary = models.CharField(max_length=50,default="")
    subCategary = models.CharField(max_length=300,default="")
    price = models.IntegerField(default=0)
    pro_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    
    def __str__(self):
        return self.pro_name