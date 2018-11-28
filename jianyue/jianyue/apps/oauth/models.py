from django.db import models
from .utils import BaseModel

class OAuthQQUser(BaseModel):

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="用户")
    openid = models.CharField(max_length=64, verbose_name="openid")

    class Meta:
        db_table = "tb_oauth_qq"
        verbose_name = "QQ登录用户"
        verbose_name_plural = verbose_name