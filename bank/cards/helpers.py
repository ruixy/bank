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
    card=Card()
    cardstatus=CardStatus()
    cardstatus.name='正常'
    card.status=cardstatus
    # print('******************************************')
    # print(type(card.balance_available))
    # print(card.balance_available)
    # print('******************************************')
    if card.status.name == '正常':
        balance_old=card.balance
        balance_new=balance_old + money
        card.balance_available=balance_new
        card.balance_freeze=0
        card.save()

        card_history=CardHistory()
        card_history.remark='''
            时间:{time},
            当前余额:{balance},
            可用余额:{available},
            冻结金额:{freeze},
        '''.format(
            time=datetime.datetime.now(),
            balance=card.balance_new,
            available=card.balance_available,
            freeze=card.balance_freeze
        )
        card_history.card=card
        card_history.operate=CardOperateType.object.get(name='存款')
        card_history.save()
    else:
        return ValueError('银行卡状态错误')


