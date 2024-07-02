# from Collectors.NewsCollectors.NewsCollector import NewsCollector
# from datetime import datetime
# from Data.GLOBAL import Data
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# import requests
# import re
# import csv
# from dateutil.relativedelta import relativedelta
# import random
# import time
# import os
#
# import signal
#
#
# class USA_NewsCollector(NewsCollector):
#     def __init__(self, batch_size):
#         super().__init__(batch_size)
#         self.api_key = "n885BvJKUNu36DFFA5eSJLkthky7bG6S"
#         self.batch_size = int(batch_size / 30)
#         self.driver_path = Data.chrome_driver_path
#         self.driver = None
#
#     def get_news(self):
#         to_write = []
#         json_prog = Data.get_progress()
#
#         date = datetime.strptime(json_prog["USA_news"], "%Y/%m")
#
#         year = date.year
#         month = date.month
#
#         for i in range(self.batch_size):
#             # url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=n885BvJKUNu36DFFA5eSJLkthky7bG6S"
#             #
#             # since = time.time()
#             # response = requests.get(url)
#
#             # print(f"response time: {time.time() - since}")
#             data = [1, 2]
#             # if response.status_code == 200:
#             if data:
#                 # data = response.json()["response"]["docs"]
#                 json_file_name = "url_list"
#                 data = Data.load_json(
#                     fr'C:\Users\Jiana\OneDrive\Desktop\ParliamentMining\DataPipeline\Data\{json_file_name}.json')
#                 if data:
#                     data = data[3350:]
#                     # json_file_name = "url_list"
#                     # with open(
#                     #         fr'C:\Users\Jiana\OneDrive\Desktop\ParliamentMining\DataPipeline\Data\{json_file_name}.json',
#                     #         'w') as f:
#                     #     json.dump(data, f)
#
#                     for index, new in enumerate(data):
#
#                         if index % 70 == 0 and index != 0:
#                             self.quit_driver()
#                             time.sleep(180)
#
#                         print(f"Process {index} from {len(data)}")
#                         title = new["abstract"]
#                         web_url = new["web_url"]
#                         since = time.time()
#                         content = self.get_body(web_url)
#                         print(f"get body time: {time.time() - since}")
#                         if content:
#                             pub_date = new["pub_date"]
#                             date_part = pub_date.split('T')[0]
#
#                             # Converting to datetime object
#                             datetime_obj = datetime.strptime(date_part, "%Y-%m-%d")
#
#                             # Formatting the date
#                             pub_date = datetime_obj.strftime("%y-%m-%d")
#
#                             to_write.append([title, pub_date, content, 1])
#                         else:
#                             print(f"content is empty ,url is {web_url}")
#                             continue
#                         random_sleep_time = random.uniform(1, 10)
#
#                         time.sleep(random_sleep_time)
#                         if index % 70 == 0 and index != 0:
#                             x = str(datetime.now()).replace(':', "-")
#                             csv_file_path = f"{Data.csv_files_dir}/news/USA/{x}.{month}.{year}.csv"
#                             with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#                                 writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
#                                 writer.writeheader()
#
#                                 writer = csv.writer(csvfile)
#                                 writer.writerows(to_write)
#                                 print("CSV file has been created successfully.")
#                                 to_write = []
#
#                     if to_write:
#                         csv_file_path = f"{Data.csv_files_dir}/news/USA/{month}.{year}.csv"
#                         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#                             writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
#                             writer.writeheader()
#
#                             writer = csv.writer(csvfile)
#                             writer.writerows(to_write)
#                             print("CSV file has been created successfully.")
#                             to_write = []
#
#                     date = date + relativedelta(months=1)
#                     year = date.year
#                     month = date.month
#                     self.quit_driver()
#                     json_prog["USA_news"] = date
#                     Data.update_progress(json_prog)
#
#                     if os.path.exists(
#                             fr'C:\Users\Jiana\OneDrive\Desktop\ParliamentMining\DataPipeline\Data\{json_file_name}.json'):
#                         os.remove(
#                             fr'C:\Users\Jiana\OneDrive\Desktop\ParliamentMining\DataPipeline\Data\{json_file_name}.json')
#
#             else:
#                 print("No data found")
#         json_prog["USA_news"] = date
#         Data.update_progress(json_prog)
#
#     def contains_special_characters1(self, my_string):
#         # Define a regular expression pattern to match any non-plain text characters
#         pattern = r'[^a-zA-Z0-9\s,.!?;:()\'\"]'
#         # Search for any matches
#         match = re.search(pattern, my_string)
#         # Return True if any matches are found, indicating the presence of special characters
#         return bool(match)
#
#     def quit_driver(self):
#         if self.driver:
#             self.driver.quit()
#             os.system("taskkill /F /IM chrome.exe")
#             self.driver = None
#
#     def init_driver(self):
#         if self.driver is None:
#             options = uc.ChromeOptions()
#             # service = Service(executable_path=Data.chrome_driver_path)
#
#             # options = Options()
#             options.add_argument('--no-sandbox')
#             options.headless = False
#             # options.add_experimental_option("prefs", prefs)
#             chrome_prefs = {
#                 "profile.default_content_setting_values": {
#                     "images": 2,
#                     "javascript": 2,
#                 }
#             }
#             options.experimental_options["prefs"] = chrome_prefs
#             driver = uc.Chrome(options=options, version_main=126,
#                                driver_executable_path=r"C:\Users\Jiana\Downloads\chromedriver-win64\chromedriver-win64"
#                                                       r"\chromedriver.exe")
#             # driver = webdriver.Chrome(options=options, service=service)
#
#             self.driver = driver
#         return self.driver
#
#     def get_body(self, url):
#         try:
#             driver = self.init_driver()
#             # service = Service(executable_path=Data.chrome_driver_path)
#             # driver = webdriver.Chrome(options=options, service=service)
#             since = time.time()
#             driver.get(url)
#             print(f"elapsed: {time.time() - since}")
#             # elements = driver.find_elements("xpath","//*")
#             body = ""
#             time.sleep(1)
#             timeout = False
#             while True:
#                 elements = driver.find_elements(By.TAG_NAME, "script")
#                 # Print the HTML source code of each element
#                 l = []
#
#                 for i in range(len(elements) - 1, -1, -1):
#                     element = elements[i]
#                     try:
#                         x = element.get_attribute('innerHTML')
#                         if "window.__preloadedData" in x:
#                             l.append(x)
#                             break
#                     except Exception as e:
#                         continue
#
#                 if l:
#                     your_string = l[-1]
#                     break
#                 else:
#                     if not timeout:
#                         time.sleep(1)
#                         timeout = True
#                         continue
#                     print(f"bad url {url}")
#                     # driver.quit()
#                     return body
#
#             # Substring to remove
#             substring_to_remove = '<script>window.__preloadedData = '
#             body = ""
#             # Remove the substring
#             modified_string = your_string.replace(substring_to_remove, '')
#
#             if not self.contains_special_characters1(modified_string):
#                 # driver.quit()
#                 # os.system("taskkill /F /IM chrome.exe")
#
#                 return modified_string
#
#             pattern = r'{"__typename":"TextInline",.*?,"text":"'
#
#             # Find all matches in the given string
#             matches = re.finditer(pattern, modified_string, re.DOTALL)
#
#             # Print the extracted texts
#             for text in matches:
#                 start_index = text.end()
#                 end_index = modified_string.find('"', start_index)
#
#                 # Ensure that the end index was found
#                 if end_index != -1:
#                     # Extract the content between the start and end indices
#                     content = modified_string[start_index:end_index]
#
#                     # Print the extracted content
#
#                     # Accumulate the content
#                     body += content
#                 else:
#                     print(f"no contentt found : {url}")
#             # driver.quit()
#             # os.system("taskkill /F /IM chrome.exe")
#             return body
#         except Exception as e:
#             print(f"Did not process {url}, driver problem")
#             json_file_name = str(datetime.now()).replace(':', "-")
#             with open(
#                     fr'C:\Users\Jiana\OneDrive\Desktop\ParliamentMining\DataPipeline\Data\news_fail\{json_file_name}.json',
#                     'w') as f:
#
#                 json.dump(url, f)
#             os.system("taskkill /F /IM chrome.exe")
#
#             return ""
#
#
# import json
#
#
# def contains_special_characters(my_string):
#     # Define a regular expression pattern to match any non-plain text characters
#     pattern = r'[^a-zA-Z0-9\s,.!?;:()\'\"]'
#     # Search for any matches
#     match = re.search(pattern, my_string)
#     # Return True if any matches are found, indicating the presence of special characters
#     return bool(match)
from Collectors.NewsCollectors.NewsCollector import NewsCollector
from datetime import datetime
from Data.GLOBAL import Data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import csv
from dateutil.relativedelta import relativedelta
import random
import time
import os

import signal


class USA_NewsCollector(NewsCollector):
    def __init__(self, batch_size):
        super().__init__(batch_size)
        self.url = "https://www.nbcnews.com/archive/articles/"
        self.batch_size = batch_size
        self.driver_path = Data.chrome_driver_path
        self.driver = None

    def get_news(self):

        json_prog = Data.get_progress()

        start_date = datetime.strptime(json_prog["USA_news"], "%Y/%m")
        new_date = start_date

        year = start_date.year
        month = start_date.strftime('%B').lower()  # Lowercase to match the input format

        counter = "2"

        to_write = []

        for i in range(self.batch_size):
            if i != 0:
                counter = "2"
                month_number = datetime.strptime(month, '%B').month
                date = datetime(int(year), month_number, 1)
                new_date = date + relativedelta(months=1)
                year = new_date.year
                month = new_date.strftime('%B').lower()  # Lowercase to match the input format

            response = requests.get(self.url + str(year) + "/" + month)

            while response.status_code == 200:
                print(month, year, counter)
                soup = BeautifulSoup(response.content, 'html.parser')

                month_elements = soup.find_all(class_='MonthPage')

                for index, element in enumerate(month_elements):
                    anchor_tags = element.find_all('a')
                    for tag in anchor_tags:
                        title = tag.text
                        href = tag.get('href')
                        if href:
                            random_sleep_time = random.uniform(0.5, 1)
                            time.sleep(random_sleep_time)
                            content, date_part = self.get_content(href)
                            if content:
                                to_write.append([title, date_part, content, 1])

                random_sleep_time = random.uniform(10, 20)
                time.sleep(random_sleep_time)

                response = requests.get(self.url + str(year) + "/" + month + "/" + counter)
                counter = str(eval(counter) + 1)

            x = str(datetime.now()).replace(':', "-")
            csv_file_path = f"{Data.csv_files_dir}/news/USA/{x}.{month}.{year}.csv"
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
                writer.writeheader()

                writer = csv.writer(csvfile)
                writer.writerows(to_write)
                print("CSV file has been created successfully.")
                to_write = []

        new_date = new_date + relativedelta(months=1)
        json_prog["USA_news"] = new_date.strftime('%Y/%m')
        Data.update_progress(json_prog)

    def get_content(self, url):
        try:
            content_response = requests.get(url)
        except Exception as e:
            print(f"passed this url {url}")
            return "", ""
        news_content = ""
        news_date = ""
        if content_response.status_code == 200:
            content_soup = BeautifulSoup(content_response.content, 'html.parser')
            content_elements = content_soup.find_all(class_='article-body__content')

            for element in content_elements:
                # Find all <p> tags within this element
                p_tags = element.find_all('p')

                # Extract the text from each <p> tag and add it to the paragraphs list
                for p in p_tags:
                    news_content += p.get_text()

            date_source_elements = content_soup.find_all(class_='article-body__date-source')
            for ele in date_source_elements:
                # Find the <time> tag within the element
                time_tag = ele.find('time')
                if time_tag and time_tag.has_attr('datetime'):
                    # Extract the datetime attribute
                    datetime_value = time_tag['datetime']
                    news_date = datetime_value.split('T')[0]

        return news_content, news_date
