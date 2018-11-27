from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers

class CreateUserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


class UserDataView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user