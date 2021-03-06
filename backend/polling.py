import time

from django.contrib.auth import get_user_model
from selenium import webdriver
import undetected_chromedriver as uc
import requests

from datetime import date
from lxml import etree

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
import django
django.setup()

from stocks.models import File, Firm
User = get_user_model()

def send_Telegram(text):
    telegram_ids = User.objects.exclude(telegram_id__isnull=True).values_list('telegram_id',flat=True)
    for id in telegram_ids:
        response = requests.post(
            f'https://api.telegram.org/bot1520040713:AAF9A_mwXznWVjgnt49yPmDy3jDkmxAGVj8/sendMessage?chat_id={id}&text={text}&'
            f'parse_mode=HTML')

def parse_send_save(accNumber,href):
    txt = requests.get(href)
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(txt.content, parser)
    issuer_cik = root.find('.//issuerCik').text.lstrip('0')
    issuer_name = root.find('.//issuerName').text
    action = root.find('.//transactionAcquiredDisposedCode/value').text
    if action == 'A':
        action_text = 'BUY'
    else:
        action_text = 'SELL'
    text = f'<b>{issuer_name}</b>, {action_text}'

    send_Telegram(text)

    raw_date = root.find('.//transactionDate/value').text
    transaction_date = date(*(int(a) for a in raw_date.split('-')))
    amount = root.find('.//transactionShares/value').text
    price = root.find('.//transactionPricePerShare/value').text
    if root.find('.//nonDerivativeTransaction') == None:
        title = 'SO'
    else:
        title = 'CS'
    try:
        firm = Firm.objects.get(pk=issuer_cik)
    except:
        firm = Firm(cik=issuer_cik,name=issuer_name)
        firm.save()
    File(accNumber=accNumber,firm=firm,transaction_date=transaction_date,amount=amount,price=price,title=title,action=action).save(force_insert=True)



driver = uc.Chrome()
accNumbers = set()

def polling():
    driver.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&count=10')
    if driver.find_element_by_xpath('html/body/div/table[2]/tbody/tr[3]/td[1]').text !='4':
        return
    href = driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]/a[2]').get_attribute('href')
    accNumber = href.split('/')[-2].lstrip('0')
    if accNumber in accNumbers :
        pass
    else:
        accNumbers.add(accNumber)
        parse_send_save(accNumber,href)

while True:
    polling()


