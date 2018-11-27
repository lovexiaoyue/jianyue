from rest_framework import serializers
from django_redis import get_redis_connection
from .models import User
import re

class CreateUserSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password2 = serializers.CharField(label="确认密码", required=True, allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label="短信验证码",required=True, allow_null=False, allow_blank=False, write_only=True)
    allow = serializers.CharField(label="同意协议", required=True, allow_blank=False, allow_null=False, write_only=True)

    def validated_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[345789]\d{9}$', value):
            raise serializers.ValidationError("手机格式错误")
        return value

    def validated_allow(self, value):
        """校验是否同意勾选"""
        if value != 'true':
            raise serializers.ValidationError("请同意用户协议")
        return value

    def validate(self, attrs):
        # 判断两次密码是否相同
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("两次密码不相同")

        # 校验短信验证码
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs['mobile']

        real_sms_code = redis_conn.get("sms_%s" %mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')

        if attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        """
        创建用户
        """
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)

        # 调用Django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }
