from io import BytesIO

import openpyxl
import pandas as pd
import xlwt
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from rest_framework.viewsets import ModelViewSet
from django_pandas.io import read_frame

# 1.实例化调度器
from djangoProject import settings
from goods.models import Goods

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 5})

# 2.调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

try:
    # 3.设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', hour='9', minute='30', second='10',id='task_time')
    # nterval 触发器
    #  参数  说明
    #  weeks (int) 间隔几周
    #  days (int)  间隔几天
    #  hours (int) 间隔几小时
    #  minutes (int)   间隔几分钟
    #  seconds (int)   间隔多少秒
    #  start_date (datetime 或 str) 开始日期
    #  end_date (datetime 或 str)   结束日期
    #  timezone (datetime.tzinfo 或str) 时区
    @register_job(scheduler, "interval", seconds=10, replace_existing=True)
    def send_email_code():
        name = []
        shop_price=[]
        myset = {
            'name':name,
            'shop_price':shop_price
        }
        for i in Goods.objects.all():
            name.append(i.name)
            shop_price.append(i.shop_price)
        myvar = pd.DataFrame(myset)
        # print(myvar)
        excelfile = BytesIO()
        myvar.to_excel(excelfile)
        excelfile.seek(0)
        email = EmailMessage()
        email.subject = 'test'
        email.body = 'context'
        email.from_email=settings.EMAIL_FROM
        email.to=["1243209334@qq.com"]
        email.attach('test_file.xls',excelfile.getvalue(),'application/ms-excel')
        email.send()


    # 4.注册定时任务
    register_events(scheduler)  # 新版本已经不需要这一步了

    # 5.开启定时任务
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()
