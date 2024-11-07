from django.db import models
from django.utils import timezone


class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True)
    climate = models.CharField(max_length=128, blank=True, null=True)
    diameter = models.IntegerField(blank=True, null=True)
    orbital_period = models.IntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    rotation_period = models.IntegerField(blank=True, null=True)
    surface_water = models.FloatField(blank=True, null=True)
    terrain = models.CharField(max_length=128, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=64)
    birth_year = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    eye_color = models.CharField(max_length=32, blank=True, null=True)
    hair_color = models.CharField(max_length=32, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE, related_name='people', null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    title = models.CharField(max_length=128, unique=True)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=64)
    producer = models.CharField(max_length=128)
    release_date = models.DateField()
    characters = models.ManyToManyField(People, related_name='movies')

    def __str__(self):
        return self.title
