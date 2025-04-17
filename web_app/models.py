from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

class Customer(models.Model):
    brand = models.CharField(max_length=255)
    tin = models.CharField(max_length=64)
    phone = models.CharField(max_length=15)

class Order(models.Model):
    customer = models.CharField(max_length=255)
    date = models.CharField(max_length=12)
    schedule = models.CharField(max_length=300)

class Archive(models.Model):
    id = models.CharField(max_length=16,primary_key=True)
    customer = models.CharField(max_length=255)
    date = models.CharField(max_length=12)
    schedule = models.CharField(max_length=300)