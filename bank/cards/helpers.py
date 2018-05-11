# -*- encoding: utf-8 -*-
from .models import Card, CardStatus, CardOperateType, CardInfo, CardHistory

import datetime

def OpenAccount():
        cardstatus = CardStatus()
        cardstatus.name = input('状态:')
        cardstatus.remark = input('备注:')
        cardstatus.save()

        card = Card()
        card.balance=input('存款金额：')
        card.balance_available=card.balance
        card.balance_freeze=0
        card.status = cardstatus
        card.save()

        cardinfo = CardInfo()
        cardinfo.name=input('姓名：')
        cardinfo.phone=input('电话号码:')
        cardinfo.emil=input('邮箱：')
        cardinfo.card = card
        cardinfo.save()

        cardoperatetype=CardOperateType()
        cardoperatetype.name=input('请输入操作:')
        cardoperatetype.remark=input('备注:')
        cardoperatetype.save()

        card_history=CardHistory()
        #card_history.time = datetime.datetime.now()
        card_history.remark='''
            银行卡:{card},
            余额:{balance}
        '''.format(
            card=card.id,
            balance=card.balance,
        )
        card_history.card=card
        card_history.operate=cardoperatetype
        card_history.save()

def deposit(card, money):
    '''
    存款
    :param card:
    :param money:
    :return:
    '''
    s_status = '正常'

    if card.status.name == s_status:
        try:
            operate = CardOperateType.objects.get(name='存款')
        except CardOperateType.DoesNotExit:
            msg='操作类型不存在'
            raise ValueError(msg)
        data_old = card.to_json()

        card.balance = card.balance+money
        card.balance_available = card.balance_available+money
        card.save()

        data_new = card.to_json()

        remark='''
        时间：{time}，
        发生金额：{money}，
        业务发生前的数据：{data_old}，
        业务发生后的数据：{data_new}，
        '''.format(
            time = datetime.datetime.now(),
            money = money,
            data_old = data_old,
            data_new = data_new,
        )
        obj = CardHistory(
            card=card,
            operate=CardOperateType.objects.get(name='存款')
        )
    else:
        msg='银行卡的状态错误.status: {}'.format(card.status.name)
        raise ValueError(msg)


def withdrawals(card, money):
    s_status = '正常'
    if card.status.name != s_status:
        msg = '银行卡状态错误.status:{}'.format(card.status.name)
        raise ValueError(msg)
    if card.balance_available > money:
        data_old = card.to_json()
        card.balance = card.balance - money
        card.balance_available = card.balance_available - money
        card.save()

        data_new = card.to_json()

        remark='''
        时间：{time}，
        发生金额：{money}，
        业务发生前的数据：{data_old}，
        业务发生后的数据：{data_new}，
        '''.format(
            time = datetime.datetime.now(),
            money = money,
            data_old = data_old,
            data_new = data_new,
        )
        obj = CardHistory(
            card=card,
            operate=CardOperateType.objects.get(name='取款')
        )
    else:
        msg = '余额不足'
        raise ValueError(msg)

