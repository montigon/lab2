from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


"""class Publisher(models.Model):
    name = models.CharField(max_length=30)
    adress  = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()"""


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return"{}".format(self.name)


class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name= "tasklists", on_delete=models.CASCADE)
    shared = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)

    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE) #blank=True, null=True)

    tag = models.ManyToManyField(Tag, blank=True)

    #owner = models.ForeignKey(User, related_name= "tasks", on_delete=models.CASCADE)


    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')

    def __str__(self):
        return "{}".format(self.name)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
