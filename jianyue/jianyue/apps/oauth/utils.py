from django.db import models
from django.conf import settings
from urllib.parse import urlencode,parse_qs
from urllib.request import urlopen
from  itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer
from itsdangerous import BadData
from jianyue.libs import constants
import re
class BaseModel(models.Model):
    """
    QQ用户基类
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 表示是一个抽象类， 用于继承，在数据库迁移时不生成新的表

class OAuthQQ(object):
    """
    QQ登录辅助工具
    """
    def __init__(self,state=None):
        self.app_id = settings.QQ_APP_ID
        self.app_key = settings.QQ_APP_KEY
        self.redirect_url = settings.QQ_REDIRECT_URL
        self.state = state or '/'

    def get_auth_url(self):
        """
        获取QQ登录地址
        :return: url地址
        """
        params = {
            "response_type":"code",
            "client_id":self.app_id,
            "redirect_uri":self.redirect_url,
            "state":self.state,
            "scope":"get_user_info"
        }
        data = urlencode(params)
        url = "https://graph.qq.com/oauth2.0/authorize?" + data
        return url

class QQUser(object):
    """
    QQ登录用户辅助工具
    """

    def __init__(self, code=None):
        self.app_id = settings.QQ_APP_ID
        self.app_key = settings.QQ_APP_KEY
        self.redirect_url = settings.QQ_REDIRECT_URL
        self.code = code

    def get_access_token(self):
        """
        获取access_token
        :return: access_token
        """
        params = {
            "grant_type":"authorization_code",
            "client_id":self.app_id,
            "client_secret":self.app_key,
            "code":self.code,
            "redirect_uri":self.redirect_url
        }

        url = "https://graph.qq.com/oauth2.0/token?" + urlencode(params)
        response = urlopen(url)
        response_data = response.read().decode()
        data = parse_qs(response_data)
        access_token = data.get('access_token',None)
        return access_token

    def get_openid(self,access_token):
        """
        获取QQ登录用户的openid
        :return: openid
        """

        url = "https://graph.qq.com/oauth2.0/me?access_token=" + access_token
        print("QQ登录地址为{}".format(url))
        response = urlopen(url)
        response_data = response.read().decode()
        openid = re.findall(r'"openid":"(.+)"', response_data)
        openid = openid[0]
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """
        生成保存用户数据的token
        :param openid: 用户的openid
        :return: token
        """
        serializer = JWTSerializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        """
        解密token
        :param token:
        :return:
        """
        serializer = JWTSerializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            return data.get('openid')