from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'users/$',views.CreateUserView.as_view()),
    url(r'authorizations/', obtain_jwt_token, name='authorizations'),
    url(r'user/$',views.UserDataView.as_view())
]