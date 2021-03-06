from selenium import webdriver

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
import django
django.setup()
from stocks.models import SIC

driver = webdriver.Chrome('/Users/f5/python/CLOUD_2020/chromedriver')
driver.get('https://www.sec.gov/info/edgar/siccodes.htm')

trs = driver.find_elements_by_xpath(
    '//*[@id="main-content"]/section/table/tbody/tr')

for tr in trs[1:]:
    tds = tr.find_elements_by_xpath('.//td')
    code = tds[0].text
    industry = tds[-1].text
    instance = SIC(sic=code,industry=industry)
    instance.save()