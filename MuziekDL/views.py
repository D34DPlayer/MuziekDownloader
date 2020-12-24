import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import SongEntry


def index(request, error_msg=None):
    latest_songs_list = SongEntry.objects.order_by("-add_date")[:5]
    context = {"latest_songs_list": latest_songs_list, "error_msg": error_msg}
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


def _entry_from_post(entry, post, key):
    if key in post:
        setattr(entry, key, post[key])


def dl_entry(request, entry_id):
    entry = get_object_or_404(SongEntry, pk=entry_id)
    return HttpResponse(f"You're at the action that will perform the download of the entry {entry_id}.")


def search(request):
    return HttpResponse("Hello, world. You're at the section where metadata will be searched.")
