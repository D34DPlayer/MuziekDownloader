import os.path

from django.conf import settings
from django.db import models

# Create your models here.


class SongEntry(models.Model):
    DL_STATUS = [
        (0, "None"),
        (1, "Pending"),
        (2, "Done"),
        (-1, "Error"),
    ]

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
    dl_status = models.IntegerField(default=0, choices=DL_STATUS)
    dl_file = models.FilePathField(path=settings.SONGS_PATH, blank=True, null=True)
    dl_error = models.CharField(max_length=64, blank=True)

    def __str__(self):
        if not (self.artist or self.track_title):
            return f"Entry {self.id}"
        else:
            name = self.track_title or "???"
            group = self.artist or "???"
            return f"{name} - {group}"

    class Meta:
        verbose_name_plural = "SongEntries"
