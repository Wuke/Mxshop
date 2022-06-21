from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


def send_email(request):
	# 想要发送的内容
    msg = '测试django发送邮箱'
    send_status = send_mail(
    		# 发送邮件的主题
            subject='请注意这是Django邮件测试',
            # 发送的内容
            message=msg,
            # 发送邮件的邮箱
            from_email=settings.EMAIL_HOST_USER,
            # 把这条邮件信息发送给xxxx@qq.com的邮箱
            recipient_list=["1961558693@qq.com"]
        )
    if send_status:
    	return HttpResponse('测试邮件已发出请注意查收')

