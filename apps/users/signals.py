from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# 用singal的方法给用户密码加密
user=get_user_model()

@receiver(post_save,sender=user)
def create_auth_token(sender,instance = None,created=False,**kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # Token.objects.create(user=instance)  用了jtw后在这就不需要了
