from django.db import models

class Admin(models.Model):
    telegram_id = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True)

class Region(models.Model):
    name = models.CharField(max_length=100)
    added_date = models.DateField(auto_now_add=True)

class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)

class Skill(models.Model):
    name = models.CharField(max_length=100)
    added_date = models.DateField(auto_now_add=True)

class Service(models.Model):
    name = models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    telegram_username = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    districts = models.ManyToManyField(District)
    skills = models.ManyToManyField(Skill)
    description = models.TextField()
    joined_date = models.DateField(auto_now_add=True)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    telegram_username = models.CharField(max_length=100)
    history = models.ManyToManyField(Service, through='History')
    joined_date = models.DateField(auto_now_add=True)

class History(models.Model):
    customer = models.ForeignKey(Customer, related_name="customer_history", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
