# -*- encoding: utf-8 -*-

from django.db import models

# Create your models here.
class CardStatus(models.Model):
    #银行卡状态
    name = models.CharField(max_length=16, verbose_name='名称')
    remark = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name

class CardOperateType(models.Model):
    #银行卡操作类型
    name = models.CharField(max_length=16, verbose_name='名称')
    remark = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name

class Card(models.Model):
    #银行卡
    ｂalance = models.FloatField(verbose_name='余额')
    balance_available = models.FloatField(verbose_name='可用金额')
    balance_freeze = models.FloatField(verbose_name='冻结金额')
    status = models.ForeignKey('CardStatus', on_delete=models.CASCADE, verbose_name='银行卡状态')

    def __str__(self):
        return '{care_id} - {balance}'.format(
            care_id=self.id,
            balance=self.ｂalance
        )

    def name(self):
        name = self.cardinfo.name
    name.short_description = '姓名'



class CardInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')
    phone = models.IntegerField(verbose_name='电话号码', blank=True)
    emil = models.EmailField(blank=True)
    card = models.OneToOneField('Card', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name



class CardHistory(models.Model):
    #银行卡流水账
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    remark = models.TextField(verbose_name='说明')
    card = models.ForeignKey('Card', on_delete=models.DO_NOTHING, verbose_name='银行卡')
    operate = models.ForeignKey('CardOperateType', on_delete=models.DO_NOTHING, verbose_name='操作')

    def __str__(self):
        return '{time} - {card_id} - {operate}'.format(
            time=self.time.isoformat(),
            card_id=self.card.id,
            operate=self.operate.name,
        )



