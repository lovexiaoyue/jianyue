from rest_framework import serializers
from .utils import QQUser

class OAuthQQUserSerializer(serializers.Serializer):
    """
    QQ登录用户创建序列化器
    """
    access_token = serializers.CharField(label="操作凭证")
    mobile = serializers.RegexField(label="手机号码",regex=r'^1[356789]\d{9}$')
    password = serializers.CharField(label="密码")
    sms_code = serializers.CharField(label="短信验证码")

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        oauth = QQUser()
        openid = oauth.check_save_user_token(access_token)
        if not openid:
            raise serializers.ValidationError("无效的access_token")