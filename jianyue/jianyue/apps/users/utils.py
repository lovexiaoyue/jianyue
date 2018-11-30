from django.core.mail import send_mail
from django.conf import settings
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

def send_verify_email(to_email, verify_url):
    """
    发送验证邮箱
    :param to_email:收件人邮箱
    :param verify_url: 验证邮箱地址
    :return:
    """
    subject = "简约商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用简约商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject,'',settings.EMAIL_FROM,[to_email],html_message=html_message)