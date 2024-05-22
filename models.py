from django.db import models

class Membership(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255,  default='')
    address = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    date_of_joining = models.DateField()
    selected_plan = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class KickboxingRegistration(models.Model):
    full_name = models.CharField(max_length=255, default='')
    date_of_joining = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    payment_option = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class ZumbaRegistration(models.Model):
    full_name = models.CharField(max_length=255, default='')
    date_of_joining = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    payment_option = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class CrossfitRegistration(models.Model):
    full_name = models.CharField(max_length=255, default='')
    date_of_joining = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    payment_option = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class YogaRegistration(models.Model):
    full_name = models.CharField(max_length=255, default='')
    date_of_joining = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    payment_option = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class Trainer(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class FreePassRequest(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    trial_date = models.DateField()

    def __str__(self):
        return self.full_name