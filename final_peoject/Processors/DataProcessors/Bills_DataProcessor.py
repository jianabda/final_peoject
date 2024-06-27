from datetime import datetime

from Processors.DataProcessors.DataProcessor import DataProcessor
from Data.GLOBAL import Data
import os
import requests
import csv


class Bills_DataProcessor(DataProcessor):
    def __init__(self, batch_size):
        super(Bills_DataProcessor, self).__init__(batch_size)

        self.data_path = Data.processor_bills_dir

        self.table = "bills"

    def to_csv(self):
        pass

    def process_data(self):
        pass

    def process_UK(self):
        pass

    def process_IL(self):
        pass

    def process_USA(self):

        counter = 0
        api_key = "c2mQmLAgAYvSIawOm9aPWLr2kYs277VUxqz6DS9L"
        file_path = os.listdir(self.data_path + '/USA')
        if len(file_path) >= 1:
            bills = Data.load_json(self.data_path + '/USA/' + file_path[0])
        else:
            print("No data to process")
            return

        next_url = []
        to_write = []
        if bills["nextPage"]:
            next_url.append(bills["nextPage"])
        for bill in bills["packages"]:  # TODO check with ayal what to do with dates and modification
            members = {}
            link = bill["packageLink"] + f"?api_key={api_key}"
            response = requests.get(link)
            if response.status_code == 200:
                summary = response.json()
                if summary["isPrivate"] == "false":
                    if summary["originChamber"] == "HOUSE":
                        chamber = "h"
                    else:
                        chamber = "s"
                    date = summary['dateIssued']
                    title = summary['title']
                    country = 1
                    id = counter
                    counter += 1
                    if summary.get("members", None):
                        for member in summary["members"]:
                            if summary.get("role", None):
                                role = member["role"]
                            else:
                                role = ""
                            if summary.get("bioGuideId", None):
                                bioGuideId = member["bioGuideId"]
                                members[bioGuideId] = role
                            else:
                                continue
                    else:
                        print("No members found")
                    bill_type = summary["docClass"]
                    congress = summary["congress"]
                    bill_number = summary["billNumber"]
                    urrrl = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/actions?api_key={api_key}"
                    response = requests.get(urrrl)
                    status = None
                    if response.status_code == 200:
                        status_data = response.json()
                        status = status_data["actions"][0]["type"]
                    to_write.append([id, title, date, members, status, country])
        if next_url:
            print("Not all data loaded")  # TODO save next url somewhere , also id counter
        # write output to csv
        csv_file_path = r"C:/Users/Jiana/OneDrive/Desktop/ParliamentMining/DataPipeline" + f'/{Data.csv_files_dir}/bills/USA/{file_path[0]}.csv'

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["bill_id", "title", "date", "sponser", "stauts", "country"])
            writer.writeheader()

            writer = csv.writer(csvfile)
            writer.writerows(to_write)

        print("CSV file has been created successfully.")

        if os.path.exists(self.data_path + '/USA/' + file_path[0]):
            os.remove(self.data_path + '/USA/' + file_path[0])

    def process_TN(self):
        pass

    def process_CA(self):  # TODO check with list longer than one
        counter = 0
        file_path = os.listdir(self.data_path + '/CA')
        if len(file_path) >= 1:
            bills = Data.load_json(self.data_path + '/CA/' + file_path[0])
        else:
            print("No data to process")
            return
        output = []
        next_url = []

        for day in bills:
            for key, value in day.items():
                if key == "pagination":
                    if value["next_url"] is not None:
                        next_url.append("https://api.openparliament.ca/" + value["next_url"])
                if key == "objects":
                    for bill in value:
                        id = counter  # TODO save counter somewhere
                        counter += 1
                        name = bill["name"]["en"]
                        date = bill["introduced"]
                        url = "https://api.openparliament.ca/" + bill["url"]
                        response = requests.get(url, headers={"Accept": "application/json"})
                        bill_data = response.json()
                        stauts = bill_data["status"]["en"]
                        is_law = bill_data["law"]
                        sposnser_url = bill_data["sponsor_politician_url"]
                        # print(sposnser_url)
                        if sposnser_url:
                            response = requests.get("https://api.openparliament.ca/" + sposnser_url,
                                                    headers={"Accept": "application/json"})
                            member_data = response.json()
                            sponser = member_data["name"]
                        else:
                            print("Sponser url is empty")
                            sponser = ""
                        # member_data = response.json()
                        # sponser = member_data["name"]
                        country = 4
                        output.append([id, name, date, sponser, stauts, country])
        if next_url:
            print("Not all data loaded")  # TODO save next url somewhere
        # write output to csv
        csv_file_path = f"{Data.csv_files_dir}/bills/CA/{str(datetime.now()).replace(':', '-')}_{file_path[0]}.csv"
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["bill_id", "title", "date", "sponser", "stauts", "country"])
            writer.writeheader()

            writer = csv.writer(csvfile)
            writer.writerows(output)
        print("CSV file has been created successfully.")

        if os.path.exists(self.data_path + '/CA/' + file_path[0]):
            os.remove(self.data_path + '/CA/' + file_path[0])
