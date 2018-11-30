from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .utils import OAuthQQ,QQUser
from . import serializers
from rest_framework.response import Response

from .models import OAuthQQUser

# Create your views here.
class OAuthQQURLView(APIView):
    """
    QQ登录地址
    """
    def get(self, request):
        state = request.query_params.get('state')
        oauth = OAuthQQ(state)
        auth_url = oauth.get_auth_url()

        return Response({"auth_url":auth_url})
class OAuthQQUserView(GenericAPIView):
    """
    QQ登录用户
    """
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"message":"缺少code参数"})
        oauth_user = QQUser(code)
        access_token = oauth_user.get_access_token()
        if access_token is None:
            return Response({"message":"服务器错误"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        access_token = access_token[0]
        openid = oauth_user.get_openid(access_token)
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            token = oauth_user.generate_save_user_token(openid)
            return Response({"access_token":token})
        else:
            # 找到用户, 生成token
            user = qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response


    """
    创建QQ登录用户信息
    """
    serializer_class = serializers.OAuthQQUserSerializer
    def post(self, request):
        """
        保存QQ登录用户信息
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            "token":token,
            "user_id":user.id,
            "username":user.username
        })
        return response