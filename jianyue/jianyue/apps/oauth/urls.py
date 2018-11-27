from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'oauth/qq/authorization/$',views.QQAuthURLView.as_view()),
    url(r'oauth/qq/user/$',views.QQAuthUserView.as_view())
]