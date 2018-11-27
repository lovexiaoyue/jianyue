from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import OAuthQQ
from .models import OAuthQQUser
from rest_framework_jwt.settings import api_settings
import logging
logger = logging.getLogger('django')
# Create your views here.
class QQAuthURLView(APIView):
    """
    登录QQ的URL
    """
    def get(self, request):
        """
        提供登录QQ的URL
        """
        state = request.query_params.get('state')
        oauth = OAuthQQ(state=state)
        auth_url = oauth.get_auth_url()
        return Response({'auth_url':auth_url},status=status.HTTP_200_OK)


class QQAuthUserView(APIView):
    """
    QQ登录用户
    """
    def get(self, request):
        """
        获取QQ登录的用户数据
        :param request:
        :return:
        """
        code = request.query_params.get('code')
        print(code)
        if not code:
            return Response({"message":"缺少code"},status=status.HTTP_400_BAD_REQUEST)
        oauth = OAuthQQ()

        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_openid(access_token)
        except Exception as e:
            logger.error(e)
            return Response({"message":"QQ服务异常"},status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            qq_user =OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoseNotExist:
            token = oauth.generate_save_user_token(openid)
            return Response({'access_token': token})
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