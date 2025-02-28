from django.db import models
from django.contrib.auth.models import User
from django.db.models import SET_NULL
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user/profile", null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
         return self.user.username



class Brands(models.Model):
    name = models.CharField(max_length=500, verbose_name="Brand nomi ")
    def __str__(self):
        return f" {self.name}"
    class  Meta:
        verbose_name_plural = "Brandlar "
        verbose_name = "Brand "

class Color(models.Model):
    color = models.CharField(max_length=100, verbose_name="Moshinaning rangi")

    def __str__(self):
        return f"{self.color}"


class Cars(models.Model):
    car_name = models.CharField(max_length=200, verbose_name="Model nomi ")
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, verbose_name="Brand nomi")
    photo = models.ImageField(upload_to="new/photos/", null=True, blank=True, verbose_name="Moshinani rasmi")
    date = models.DateField(null=True, blank=True, verbose_name="Ishlab chirqarilgan vaqti")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)


    def __str__(self):
        return f"{self.car_name} {self.brand} {self.date} {self.color}"
    class  Meta:
        verbose_name_plural = "Moshinalar "
        verbose_name = "Moshina "

class Comment(models.Model):
    text = models.TextField(verbose_name="Dars haqida firkingizni qoldiring ")
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True )


    def __str__(self):
        return f"{self.user.username}"