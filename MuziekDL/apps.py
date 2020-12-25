import os

from django.apps import AppConfig
from django.conf import settings


class MuziekdlConfig(AppConfig):
    name = 'MuziekDL'

    def ready(self):
        if os.path.exists(settings.SONGS_PATH):
            for name in os.listdir(settings.SONGS_PATH):
                os.remove(os.path.join(settings.SONGS_PATH, name))
        else:
            os.mkdir(settings.SONGS_PATH)

        self.get_model("SongEntry").objects.all().update(dl_status=0)
