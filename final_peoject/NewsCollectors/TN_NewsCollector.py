from selenium.common.exceptions import TimeoutException
from Collectors.NewsCollectors.NewsCollector import NewsCollector
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.wait import WebDriverWait
from Data.GLOBAL import Data
from datetime import datetime
import csv


##################################################
# NOTES:
# HAS TO WORK WITH HEADLESS TRUE
# HAS NO BATCH SIZE
##################################################
class TN_NewsCollector(NewsCollector):
    def __init__(self, batch_size):
        super().__init__(batch_size)
        self.url = "https://www.africanews.com/country/tunisia/"
        self.driver_path = r"C:\Users\Jiana\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    def get_news(self):
        json_prog = Data.get_progress()
        last_date = datetime.strptime(json_prog["TN_news"], "%Y/%m%d")
        to_write = []

        options = Options()
        options.headless = False
        seen = {}
        driver = webdriver.Chrome(options=options, executable_path=self.driver_path)

        response = requests.get(self.url)
        driver.get(self.url)
        click = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/span")
        click.click()
        exist = True
        stop = False
        # Check if the request was successful
        while exist:
            if response.status_code == 200:
                try:
                    view_more_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#main > div > div.layout.theme-block__spacer > "
                                                        "div.layout.view-more-bar.btn--container.theme--news > div > a"))
                    )
                    view_more_button.click()
                except TimeoutException:
                    exist = False
                source = driver.page_source
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(source, 'html.parser')

                # Find the div with class 'main-content'
                main_content = soup.find('div', class_='main-content')

                # Extract all href attributes from a tags within the main-content div
                links = main_content.find_all('a', href=True)
                to_process = []
                for link in links:
                    if link["href"] not in seen:
                        seen[link["href"]] = 1
                        to_process.append(link["href"])
                to_process = set(to_process)
                to_process = list(to_process)

                for href in to_process:
                    content = ""
                    title = ""
                    date = ""
                    response = requests.get("https://www.africanews.com" + href)
                    if response.status_code == 200 and href != "/country/tunisia/":
                        soup1 = BeautifulSoup(response.text, 'html.parser')
                        h1_tag = soup1.find('h1')
                        if h1_tag:
                            title = h1_tag.get_text()
                        else:
                            print("No title found!")
                        time_element = soup1.find('time', class_='article__date')
                        if time_element and 'datetime' in time_element.attrs:
                            datetime_value = time_element['datetime']
                            date_part = datetime_value.split(' ')[0]  # Extract the date part
                            date = date_part
                            curr_date = datetime.strptime(date, "%Y-%m-%d")
                            if curr_date <= last_date:
                                stop = True
                                break
                            else:
                                max_date = curr_date

                        target_div = soup1.find('div',
                                                class_='article-content__text article-content__left-column '
                                                       'js-responsive-iframes-container')
                        p_tags = target_div.find_all('p')
                        for i, p_tag in enumerate(p_tags, 1):
                            content += p_tag.get_text()
                        to_write.append([title, date, content, 5])
                if stop:
                    break

        csv_file_path = f"{Data.csv_files_dir}/news/TN{str(datetime.now()).replace(':', '-')}"
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["title", "date", "content", "country"])
            writer.writeheader()

            writer = csv.writer(csvfile)
            writer.writerows(to_write)
            print("CSV created")
        # update
        last_date = max_date
        json_prog["TN_news"] = last_date.strftime("%Y-%m-%d")
        Data.update_progress(json_prog)
