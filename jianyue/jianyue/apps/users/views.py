from rest_framework.generics import CreateAPIView
from . import serializers

class CreateUserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer