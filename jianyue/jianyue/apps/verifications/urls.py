from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>.+)/$', views.ImageCodeView.as_view()),
    url(r'^sms_codes/(?P<mobile>.+)/$', views.SMSCodeView.as_view()),
    url(r'^usernames/(?P<username>.{5,20})/count/$',views.UserCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[345789]\d{9})/count/$',views.MobileCountView.as_view()),
]