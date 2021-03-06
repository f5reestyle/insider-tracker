
import django
from multiprocessing import Queue, cpu_count
from threading import Thread
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from numpy.random import randint
import pandas as pd
import logging

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
django.setup()
from stocks.models import Firm, Stock

logger = logging.getLogger(__name__)
no_cik = []

ticker_data = pd.read_csv('/Users/f5/dev/nasdaq_20210222.csv')
TICKERS = list(ticker_data['Symbol'])

selenium_data_queue = Queue()
worker_queue = Queue()

worker_ids = list(range(cpu_count()))


selenium_workers = {i: uc.Chrome() for i in worker_ids}
for worker_id in worker_ids:
    worker_queue.put(worker_id)


def selenium_task(worker, ticker):

    worker.set_window_size(randint(100, 200), randint(200, 400))
    logger.info("Getting Google")
    worker.get(f'https://sec.report/Ticker/{ticker}')

    try:
        cik = worker.find_element_by_xpath(
            '/html/body/div[1]/div/h2[1]').text.split()[-1]
    except:
        no_cik.append(ticker)
        Stock(ticker=ticker, exchange='NASDAQ').save()
        return
    try:
        firm = Firm.objects.get(pk=cik)
    except:
        name = worker.find_element_by_xpath(
            '/html/body/div[1]/div/h1').text.split(':')[-1].lstrip()
        sic1 = worker.find_elements_by_xpath(
            '/html/body/div[1]/div/div[3]/div[2]/table/tbody/tr[6]/td')
        if sic1 != [] and sic1[0].text == 'SIC':
            sic = sic1[1].text.split()[0]
        else:
            sic2 = worker.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/table/tbody/tr[5]/td')
            if sic2 != [] and sic2[0].text == 'SIC':
                sic = sic2[1].text.split()[0]
            else:
                sic3 = worker.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[4]/div[2]/table/tbody/tr[6]/td')
                if sic3 != [] and sic3[0].text == 'SIC':
                    sic = sic3[1].text.split()[0]
                else:
                    sic4 = worker.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[4]/div[2]/table/tbody/tr[5]/td')
                    if sic4 != [] and sic4[0].text == 'SIC':
                        sic = sic4[1].text.split()[0]
                    else:
                        sic = 9999
        firm = Firm(cik=cik, name=name, sic_id=int(sic))
        firm.save()

    Stock(ticker=ticker, firm=firm, exchange='NASDAQ').save()

def selenium_queue_listener(data_queue, worker_queue):

    logger.info("Selenium func worker started")
    while True:
        try:
            current_data = data_queue.get(timeout=1)
            logger.info(f"Got the item {current_data} on the data queue")
        except:
            logger.warning("STOP encountered, killing worker thread")

            break

        # Get the ID of any currently free workers from the worker queue
        worker_id = worker_queue.get()
        worker = selenium_workers[worker_id]
        # Assign current worker and current data to your selenium function
        selenium_task(worker, current_data)
        # Put the worker back into the worker queue as  it has completed it's task
        worker_queue.put(worker_id)
    return


# Create one new queue listener thread per selenium worker and start them
logger.info("Starting selenium background processes")
selenium_processes = [Thread(target=selenium_queue_listener,
                             args=(selenium_data_queue, worker_queue)) for _ in worker_ids]
for p in selenium_processes:
    p.daemon = True
    p.start()

# Add each item of data to the data queue, this could be done over time so long as the selenium queue listening
# processes are still running
logger.info("Adding data to data queue")
for d in TICKERS:
    try:
        Stock.objects.get(ticker=d)
    except:
        selenium_data_queue.put(d)

# Wait for all selenium queue listening processes to complete, this happens when the queue listener returns
logger.info("Waiting for Queue listener threads to complete")
for p in selenium_processes:
    p.join()

# Quit all the web workers elegantly in the background
logger.info("Tearing down web workers")
for b in selenium_workers.values():
    b.quit()

print('no_cik : ', no_cik)
