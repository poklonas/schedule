from django.conf.urls import url

from . import views

app_name = 'schedule'
urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^(?P<user_id>[0-9]+)', views.user_page, name='user_page')
]
