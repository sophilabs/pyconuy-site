from django.conf.urls import *

urlpatterns = patterns('main.views',
    url(r"^$", 'index', name='index'),
    url(r"^proposal$", 'proposal_add', name='proposal_add'),
    url(r"^proposal-sent$", 'proposal_sent', name='proposal_sent'),
    url(r"^schedule$", 'schedule', name='schedule'),
)