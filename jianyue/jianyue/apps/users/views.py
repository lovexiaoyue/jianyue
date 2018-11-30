from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import User
from rest_framework import status
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

class EmailVerifyView(APIView):
    """
    邮箱验证
    """
    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"message":"缺少token"},status=status.HTTP_400_BAD_REQUEST)
        # 验证token
        user = User.check_verify_email_token(token=token)
        if user is None:
            return Response({"message":"无效的连接"},status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({"message":"OK"})
