from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 1.实例化调度器
from djangoProject import settings

scheduler = BackgroundScheduler()

# 2.调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

try:
    # 3.设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler, "interval", seconds=10, replace_existing=True)
    def send_email_code():
        email = EmailMessage(
            subject='验证码',
            body='123',
            from_email=settings.EMAIL_HOST_USER,
            to=['1243209334@qq.com',]
        )
        email.fail_silently = False
        email.send()


    # 4.注册定时任务
    register_events(scheduler)  # 新版本已经不需要这一步了

    # 5.开启定时任务
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()
