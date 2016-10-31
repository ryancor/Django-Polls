from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'polls/registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/polls/registration/login.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^search_results/$', views.search_results, name='search_results'),
    url(r'^.*$', RedirectView.as_view(url='/polls/', permanent=False), name='index'),
]
