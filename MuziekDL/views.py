import re
import os

from django.views.static import serve
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Q

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

    old_entry = None
    if 'entry_id' in request.POST:
        old_entry = _get_object_or_none(SongEntry, pk=request.POST["entry_id"])

    duplicate = [_entry_from_post(entry, request.POST, key, old_entry) for key in keys]

    if all(duplicate):
        del entry
        return HttpResponseRedirect(reverse('download_entry', args=(old_entry.id,)))
    else:
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


class SearchResultsView(ListView):
    model = SongEntry
    template_name = 'MuziekDL/search.html'
    context_object_name = 'entry_list'

    def get_queryset(self):
        search = self.request.GET.get("search", default="")
        return SongEntry.objects.filter(
            Q(track_title__icontains=search) |
            Q(genre__icontains=search) |
            Q(artist__icontains=search)
        )


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
def _entry_from_post(entry, post, key, old_entry=None):
    value = post.get(key, default="")
    if value != "":
        setattr(entry, key, post[key])

    if old_entry:
        return value == str(getattr(old_entry, key))
    return False


def _get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
