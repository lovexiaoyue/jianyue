from rest_framework import serializers
from .utils import QQUser
from django_redis import get_redis_connection
from users.models import User
from .models import OAuthQQUser
class OAuthQQUserSerializer(serializers.Serializer):
    """
    QQ登录用户创建序列化器
    """
    access_token = serializers.CharField(label="操作凭证")
    mobile = serializers.RegexField(label="手机号码",regex=r'^1[356789]\d{9}$')
    password = serializers.CharField(label="密码")
    sms_code = serializers.CharField(label="短信验证码")

    def validate(self, attrs):
        # 校验access_token
        access_token = attrs.get('access_token')
        oauth = QQUser()
        openid = oauth.check_save_user_token(access_token)
        if not openid:
            raise serializers.ValidationError("无效的access_token")
        attrs['openid'] = openid
        # 校验短信验证码
        mobile = attrs['mobile']
        sms_code = attrs.get('sms_code')
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" %mobile)
        if not real_sms_code:
            raise serializers.ValidationError("无效的短信验证码")
        if real_sms_code.decode()!= sms_code:
            raise serializers.ValidationError("短信验证码错误")
        # 如果用户存在验证密码
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError("密码错误")
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            user = User.objects.create_user(
                username=validated_data.get('mobile'),
                password=validated_data['password'],
                mobile=validated_data['mobile']
            )
        openid = validated_data['openid']
        try:
            openid = OAuthQQUser.objects.get(openid=openid)
        except Exception:
            OAuthQQUser.objects.create(
                openid=openid,
                user=user
            )
        return user