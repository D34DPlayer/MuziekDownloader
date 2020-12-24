from django.db import models

# Create your models here.


class SongEntry(models.Model):
    song_identifier = models.CharField(max_length=32)
    album = models.CharField(max_length=64, blank=True)
    artist = models.CharField(max_length=64, blank=True)
    genre = models.CharField(max_length=64, blank=True)
    artwork_url = models.CharField(max_length=256, blank=True)
    track_number = models.IntegerField(blank=True, null=True)
    total_tracks = models.IntegerField(blank=True, null=True)
    track_title = models.CharField(max_length=128, blank=True)
    year = models.IntegerField("year published", blank=True, null=True)
    add_date = models.DateTimeField("date entry added")
