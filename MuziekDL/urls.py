from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/<str:song_identifier>/', views.dl_form, name='form'),
    path('<int:entry_id>/', views.dl_form, name='form_id'),
    path('download/', views.dl_add_entry, name='download'),
    path('<int:entry_id>/download/', views.dl_entry, name='download_entry'),
    path('parse/', views.parse_identifier, name='parse_id'),
    path('search/', views.search, name="search"),
    # AJAX
    path('<int:entry_id>/ajax/start_download', views.ajax_start_download, name="ajax_start_download"),
    path('<int:entry_id>/ajax/status', views.ajax_get_download_progress, name="ajax_status"),
    path('<int:entry_id>/ajax/download', views.ajax_download_link, name="ajax_download"),
]