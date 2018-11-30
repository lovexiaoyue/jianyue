from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
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

class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    """
    serializer_class = serializers.EmailSerialize
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # self　表示当前视图对象
        # self.request 这个表示当前客户端的请求对象
        return self.request.user