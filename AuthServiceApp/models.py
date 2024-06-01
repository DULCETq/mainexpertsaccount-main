from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model):
    types = (('Client', 'Client'),
             ('Expert', 'Expert'),
             ('Admin', 'Admin'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Account')
    name = models.CharField(max_length=100, verbose_name='Full name', null=True, blank=True)
    user_type = models.CharField(max_length=100, verbose_name='user type', choices=types)
    phone = models.CharField(max_length=20, verbose_name='Phone')
    age = models.IntegerField(verbose_name='Age', null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Account is active", default=True)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Balance')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    avatar = models.FileField(null=True, blank=True)


class Education(models.Model):
    types = (('General education', 'General'),
             ('Bachelor', 'Bachelor'),
             ('Master', 'Master'),
             ('PhD', 'PhD'),
             ('MBA', 'MBA'),
             ('Course', 'Course'))
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Client')
    education_type = models.CharField(max_length=100, verbose_name='education type', choices=types)
    place_of_study_name = models.CharField(max_length=100, verbose_name='Place of study name')
    date_start = models.DateField(verbose_name='Date of start')
    date_end = models.DateField(verbose_name='Date of end')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserCalendar(models.Model):
    levels = (('Convenient', 'Convenient'),
              ('Barely convenient', 'Barely convenient'),
              ('Not convenient', 'Not convenient'),)
    weekdays = (('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'))

    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Client')
    weekday = models.CharField(max_length=100, verbose_name='weekday', choices=weekdays)
    convenience_level = models.CharField(max_length=100, verbose_name='weekday', choices=levels)
    time_start = models.TimeField(verbose_name='Time of start')
    time_end = models.TimeField(verbose_name='Time of end')
    is_available = models.BooleanField(verbose_name='Is available')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Expert(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Account')
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=100, blank=True), null=True, blank=True)
    personal_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='personal info')
    additional_info = models.CharField(max_length=255, null=True, blank=True, verbose_name='additional info')
    rating = models.FloatField(default=4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ExpertCalendar(models.Model):
    levels = (('Comfort', 'Comfort'),
              ('Possible', 'Possible'),
              ('Only emergency', 'Only emergency'))
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name='Expert')
    day = models.CharField(max_length=255, null=True, blank=True, verbose_name='Day of week')
    time_start = models.TimeField(verbose_name='Time of start')
    time_end = models.TimeField(verbose_name='Time of end')
    comfortable = models.CharField(max_length=255, choices=levels)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ExpertExperience(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name='Expert')
    workplace = models.CharField(max_length=255, null=True, blank=True, verbose_name='Workplace')
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name='Position')
    date_start = models.DateField(verbose_name='Date of start')
    date_end = models.DateField(verbose_name='Time of end')
    duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='Duration')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Description')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Client(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Account', related_name='Account')
    role = models.CharField(max_length=60, default='learner')
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    location_2_address = models.CharField(max_length=255, null=True, blank=True)
    location_2_name = models.CharField(max_length=255, null=True, blank=True)
    personal_description = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    goals = ArrayField(models.CharField(max_length=100, blank=True), null=True, blank=True)
    fav_lessons = ArrayField(models.CharField(max_length=100, blank=True), null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class LinkedAccount(models.Model):
    user_initiator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='initiator user',
                                       related_name='user_initiator')
    user_linked = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='linked user',
                                    related_name='user_linked')
    initiator_role = models.CharField(max_length=50, null=True, blank=True)
    linked_role = models.CharField(max_length=50, null=True, blank=True)
