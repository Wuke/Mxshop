# Generated by Django 2.2.28 on 2022-06-22 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verifycode',
            options={'verbose_name': '邮箱验证码', 'verbose_name_plural': '邮箱验证码'},
        ),
    ]
