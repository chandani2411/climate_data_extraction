from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^download_files', views.download_files, name='download_files'),
    url(r'^yearwise_data', views.yearwise_data, name='yearwise_data'),
    url(r'^export_csv/(?P<id>.*)$', views.export_csv, name='export_csv'),


   ]