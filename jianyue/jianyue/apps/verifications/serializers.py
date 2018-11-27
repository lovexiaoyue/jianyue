from rest_framework import serializers
from django_redis import get_redis_connection
import logging

logger = logging.getLogger('django')

class ImageCodeCheckSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器
    """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']

        # 查询验证码
        redis_conn = get_redis_connection("verify_codes")
        r_code = redis_conn.get("img_%s" %image_code_id)
        if not r_code:
            raise serializers.ValidationError('图片验证码无效')
        try:
            redis_conn.delete("img_%s" % image_code_id)
        except Exception as e:
            logger.error(e)
        # 进行比对
        r_code = r_code.decode()
        if r_code.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')
        # 检测是否在60S内
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get("send_flag_%s" %mobile)
        if send_flag:
            raise serializers.ValidationError('请求过于频繁')

        return attrs





