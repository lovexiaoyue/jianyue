from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .utils import OAuthQQ,OAuthQQUser
from rest_framework.response import Response
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
class OAuthQQUserView(APIView):
    """
    QQ登录用户
    """
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"message":"缺少code参数"})
        oauth_user = OAuthQQUser(code)
        access_token = oauth_user.get_access_token()
        if access_token is None:
            return Response({"message":"服务器错误"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        access_token = access_token[0]
        openid = oauth_user.get_openid(access_token)
        print(openid)