
from django.db import models

class Template(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
        return self.name

class product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    catagory = models.CharField(max_length=50,default="")
    price = models.IntegerField()
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to="images",default="")

    def __str__(self):
        return self.productName


    
class Contact(models.Model):
    contactId= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name

