import re
import os

from django.views.static import serve
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .models import SongEntry
from .libs.downloader import SongDownloader


def index(request):
    latest_songs_list = SongEntry.objects.order_by("-add_date")[:5]
    context = {"latest_songs_list": latest_songs_list}
    return render(request, "MuziekDL/index.html", context)


def dl_form(request, entry_id=None, song_identifier=None):
    context = {}
    if entry_id is not None:
        entry = get_object_or_404(SongEntry, pk=entry_id)
        context["entry"] = entry
    elif song_identifier is not None:
        context["song_identifier"] = song_identifier
    else:
        raise Http404("Page not found.")

    return render(request, "MuziekDL/download_form.html", context)


def dl_add_entry(request):
    keys = [
        "album", "artist", "genre", "artwork_url", "track_number",
        "total_tracks", "track_title", "track_title", "year",
    ]

    if 'song_identifier' not in request.POST:
        raise Http404(f"No song identifier was provided.")
    entry = SongEntry(song_identifier=request.POST["song_identifier"], add_date=timezone.now())

    for key in keys:
        _entry_from_post(entry, request.POST, key)

    entry.save()
    return HttpResponseRedirect(reverse('download_entry', args=(entry.id,)))


def parse_identifier(request):
    pattern = "^.*?(?:youtu.be\\/|v\\/|\\/u\\/\\w\\/|embed\\/|watch\\?)\\??v?=?([^#&?]*).*$"

    if 'search' not in request.POST:
        return HttpResponseRedirect(reverse('index'))
    else:
        re_query = re.search(pattern, request.POST["search"])
        if not re_query:
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('form', args=(re_query.group(1),)))


def dl_entry(request, entry_id):
    entry = get_object_or_404(SongEntry, pk=entry_id)
    return render(request, "MuziekDL/download_action.html", {"entry": entry})


def search(request):
    return HttpResponse("You're at the section where metadata will be searched.")


# AJAX HANDLING
def ajax_start_download(request, entry_id):
    entry = _get_object_or_none(SongEntry, pk=entry_id)
    if not entry:
        return JsonResponse({"success": 0, "error": "Entry not found."})
    elif entry.dl_status == 1:
        return JsonResponse({"success": 1, "message": "Download already started."})
    elif entry.dl_status == 2:
        return JsonResponse({"success": 1, "message": "Download already completed."})
    else:  # If no download yet or the last one failed.
        entry.dl_status = 1
        entry.save()
        dl = SongDownloader()
        if not dl.fetch_song(f"youtu.be/{entry.song_identifier}"):
            entry.dl_status = -1
            entry.error_msg = "Invalid song identifier."
            entry.save()
            return JsonResponse({"success": 0, "message": "Wrong identifier."})
        else:
            dl.download_song(entry)
            return JsonResponse({"success": 1, "message": "Download started."})


def ajax_get_download_progress(request, entry_id):
    entry = _get_object_or_none(SongEntry, pk=entry_id)
    if not entry:
        return JsonResponse({"success": 0, "error": "Entry not found."})
    elif entry.dl_status == 2:
        return JsonResponse({"success": 1, "dl_status": 2, "dl_url": entry.dl_file})
    elif entry.dl_status == -1:
        return JsonResponse({"success": 1, "dl_status": -1, "dl_error": entry.dl_error})
    else:
        return JsonResponse({"success": 1, "dl_status": entry.dl_status})


def ajax_download_link(request, entry_id):
    dl = SongDownloader()
    if dl.is_downloaded(entry_id):
        path = dl.get_song_path(entry_id)
        return serve(request, os.path.basename(path), os.path.dirname(path))
    else:
        raise Http404("Song not found.")


# UTILS
def _entry_from_post(entry, post, key):
    if key in post:
        setattr(entry, key, post[key])


def _get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
