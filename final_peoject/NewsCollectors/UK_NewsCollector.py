from Collectors.NewsCollectors.NewsCollector import NewsCollector
from datetime import datetime, timedelta
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
from Processors.DataProcessors.DataProcessor import DataProcessor
import pickle
import os
import json
import pandas as pd
from Data.GLOBAL import Data
from Collectors.DataCollectors.CA_DataCollector import CA_DataCollector
import csv
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.wait import WebDriverWait
import re
from bs4 import BeautifulSoup
import json
import csv
from Data.GLOBAL import Data


class UK_NewsCollector(NewsCollector):
    def __init__(self, batch_size):
        super().__init__(batch_size)
        self.driver_path = r"C:\Users\Jiana\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
        self.api_key = "822ef1d1-f75f-4ecb-a8da-33f326917d2a"
        self.url = 'http://content.guardianapis.com/search'
        self.parm = {
            'from-date': "",
            'to-date': "",
            'order-by': "newest",
            'show-fields': 'all',
            'page-size': 200,
            'api-key': self.api_key
        }

    def get_news(self):
        output = []
        json_prog = Data.get_progress()
        start_date = json_prog["UK_news"]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=self.batch_size)

        dayrange = range((end_date - start_date).days + 1)
        for daycount in dayrange:
            dt = start_date + timedelta(days=daycount)
            datestr = dt.strftime('%Y-%m-%d')
            # then let's download it
            all_results = []
            self.parm['from-date'] = datestr
            self.parm['to-date'] = datestr
            current_page = 1
            total_pages = 1
            while current_page <= total_pages:
                self.parm['page'] = current_page
                resp = requests.get(self.url, self.parm)
                print(resp.status_code)
                data = resp.json()
                if data.get("response", None):
                    all_results.extend(data['response']['results'])
                    # if there is more than one page
                    total_pages = data['response']['pages']
                current_page += 1

            for new in all_results:
                title = new["webTitle"]
                if new.get("fields", None):
                    cleaned_text = re.sub(r'<[^>]+>', '', new["fields"]["body"])
                    output.append([title, datestr, cleaned_text, 2])

            if daycount % 30 == 0 and daycount != 0 and len(output) > 0:
                year = dt.year
                month = dt.month
                csv_file_path = f"{Data.csv_files_dir}/news/UK/{year}_{month}.csv"
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
                    writer.writeheader()

                    writer = csv.writer(csvfile)
                    writer.writerows(output)
                    output = []
                    print("CSV file has been created successfully.")

        if output:
            year = end_date.year
            month = end_date.month

            csv_file_path = f"{Data.csv_files_dir}/news/UK/{year}_{month}.csv"

            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
                writer.writeheader()

                writer = csv.writer(csvfile)
                writer.writerows(output)
                print("CSV file has been created successfully.")

        json_prog["UK_news"] = end_date.strftime("%Y-%m-%d")
        Data.update_progress(json_prog)
