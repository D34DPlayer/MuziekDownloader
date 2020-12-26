from django.contrib import admin

# Register your models here.

from .models import SongEntry


admin.site.register(SongEntry)
