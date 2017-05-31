from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    ]















#
# urlpatterns = [
#     url(r'^$', views.index),
#     url(r'^register$', views.register_account),
#     url(r'^login$', views.login_account),
#     url(r'^logout$', views.logout),
#     url(r'^travels$', views.travels),
#     url(r'^travels/add$', views.add_travel),
#     url(r'^trip_add$', views.trip_add),
#     url(r'^travels/destination/(?P<id>\d+)$', views.destination, name = 'destination'),
#     url(r'^travels/join/(?P<id>\d+)$', views.join_trip, name = 'join'),
#     url(r'^not_logged$', views.not_logged),
# ]
