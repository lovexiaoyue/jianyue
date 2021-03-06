from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer
from itsdangerous import BadData
from django.conf import settings
from jianyue.libs import constants
from django.db import models
class User(AbstractUser):
    """用户模型类"""


    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


    def generate_verify_email_url(self):
        """
        生成邮箱验证的url
        :return:
        """
        serializer = JWTSerializer(settings.SECRET_KEY,expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data = {"user_id":self.id,"email":self.email}
        token = serializer.dumps(data).decode()
        verify_url = 'http://www.lovexiaoyue.com:8080/success_verify_email.html?token=' + token
        return verify_url

    @staticmethod
    def check_verify_email_token(token):
        """
        检查验证邮件的token
        """
        serializer = JWTSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            email = data.get('email')
            user_id = data.get('user_id')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user

