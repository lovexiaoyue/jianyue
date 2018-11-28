from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^oauth/qq/authorization/$', views.OAuthQQURLView.as_view()),
    url(r'^oauth/qq/user/$',views.OAuthQQUserView.as_view())
]