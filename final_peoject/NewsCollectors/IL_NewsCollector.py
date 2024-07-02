import random

from Collectors.NewsCollectors.NewsCollector import NewsCollector
from datetime import datetime
from datetime import date
import time
from Data.GLOBAL import Data
import requests
import re
from bs4 import BeautifulSoup
import csv
from dateutil.relativedelta import relativedelta
import os


class IL_NewsCollector(NewsCollector):
    def __init__(self, batch_size):
        super().__init__(batch_size)
        self.driver_path = r"C:\Users\Jiana\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
        self.batch_size = int(batch_size / 30)

    def get_news(self):
        to_write = []
        json_prog = Data.get_progress()
        # print(json_prog["IL_news"])

        date = datetime.strptime(json_prog["IL_news"], "%Y/%m")

        year = date.year
        month = date.month

        for i in range(self.batch_size):
            print(f"Now process {month}-{year}")
            counter = 1
            url = f"https://news.walla.co.il/archive/5109?month={month}&page={counter}&year={year}"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            while response.status_code == 200:
                print(f"now in page {counter}")
                div_elements = soup.find('div', class_='css-2xya7t')
                li_elements = div_elements.find_all('li')

                for li in li_elements:
                    content = ""
                    link = li.find("a").get('href')
                    try:
                        response1 = requests.get(link)
                    except Exception as e:
                        print(f"bad link {link}")
                        continue
                    soup1 = BeautifulSoup(response1.text, 'html.parser')

                    title = soup1.find('h1', class_='article_speakable')
                    if title:
                        title = title.get_text()
                    else:
                        title = "unknown"

                    date_element = soup1.find(class_='date-and-time-p')
                    if date_element:
                        date_text = date_element.get_text(strip=True)
                        match = re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', date_text)
                        extracted_date = match.group(0)
                        extracted_date = datetime.strptime(extracted_date, '%d.%m.%Y')
                        news_date = extracted_date.strftime('%Y-%m-%d')
                    else:
                        news_date = "unknown"

                    sections = soup1.find_all('section', class_='css-19nosoq')

                    for section in sections:
                        if section:
                            content += section.get_text()
                        else:
                            content = "unknown"
                            break
                    if content != "unknown":
                        to_write.append([title, news_date, content, 3])

                counter += 1
                url = f"https://news.walla.co.il/archive/5109?month={month}&page={counter}&year={year}"
                response = requests.get(url)

            random_sleep_time = random.uniform(1, 4)
            time.sleep(random_sleep_time)
            csv_file_path = f"{Data.csv_files_dir}/news/IL/{month}_{year}.csv"

            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
                writer.writeheader()

                writer = csv.writer(csvfile)
                writer.writerows(to_write)
                print("CSV file has been created successfully.")

            to_write = []

            date = date + relativedelta(months=1)
            year = date.year
            month = date.month

        last_date = date
        json_prog["IL_news"] = last_date.strftime("%Y/%m")
        Data.update_progress(json_prog)
