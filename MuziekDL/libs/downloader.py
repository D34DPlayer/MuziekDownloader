import os
import logging
import threading
from urllib.request import urlopen
from urllib.error import HTTPError

import music_tag
import youtube_dl

from django.conf import settings

default_config = {
    "quiet": True,
    "format": "bestaudio/best",
    "postprocessors": [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    "ignoreerrors": True,
    "no_color": True,
    "logger": logging.getLogger("django.download")
}


def _set_error(entry, msg):
    entry.dl_status = -1
    entry.error_msg = msg
    entry.save()


class SongDownloader(youtube_dl.YoutubeDL):
    def __init__(self):
        self._video_info = None
        self._download_dir = os.path.abspath(settings.SONGS_PATH)
        if not os.path.exists(self._download_dir):
            os.mkdir(self._download_dir)

        super().__init__(default_config)

    def fetch_song(self, url: str):
        info = self.extract_info(url=url, download=False)
        self._video_info = info
        return info

    def download_song(self, entry):
        thread = threading.Thread(target=self._download_song, args=(entry,))
        thread.start()
        return thread

    def _download_song(self, entry):
        if not self._video_info:
            _set_error(entry, "Download before fetch.")

        file_name = f'{entry.id}.%(ext)s'
        self.params["outtmpl"] = os.path.join(self._download_dir, file_name)

        self.prepare_filename(self._video_info)
        self.download([self._video_info["url"]])

        self.update_metadata(entry)

        entry.dl_status = 2
        entry.dl_file = self.get_song_path(entry.id)
        entry.save()

    def is_downloaded(self, song_id: int):
        return bool(self.get_song_path(song_id))

    def update_metadata(self, entry):
        song_path = self.get_song_path(entry.id)

        if song_path:
            f = music_tag.load_file(song_path)
            f['artist'] = entry.artist
            f['genre'] = entry.genre
            f['track_title'] = entry.track_title
            f['album'] = entry.album
            f['track_number'] = entry.track_number
            f['total_tracks'] = entry.total_tracks
            f['year'] = str(entry.year)

            if entry.artwork_url:
                try:
                    with urlopen(entry.artwork_url) as img_in:
                        f['artwork'] = img_in.read()
                except TypeError:
                    pass
                except HTTPError:
                    pass

            f.save()

    def get_song_path(self, song_id):
        path = os.path.join(self._download_dir, f"{song_id}.mp3")
        return path if os.path.exists(path) else None
