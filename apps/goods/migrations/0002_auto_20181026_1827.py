# Generated by Django 2.0 on 2018-10-26 10:27

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='goods_desc',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='内容'),
        ),
        migrations.AddField(
            model_name='goodscategroybrand',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品类目'),
        ),
    ]
