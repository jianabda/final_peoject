import csv
from datetime import datetime

from Processors.DataProcessors.DataProcessor import DataProcessor
import pickle
import os
import json
import pandas as pd
from Data.GLOBAL import Data

converter = {  # date format yyyy-mm-dd
    118: {  # start date    # end date
        'Session 1': ['2023-01-03', '2024-01-03'],
        'Session 2': ['2024-01-03', None]
    },
    117: {
        'Session 1': ['2021-01-03', '2022-01-03'],
        'Session 2': ['2022-01-03', '2023-01-03']
    },
    116: {
        'Session 1': ['2019-01-03', '2020-01-03'],
        'Session 2': ['2020-01-03', '2021-01-03']
    },
    115: {
        'Session 1': ['2017-01-03', '2018-01-03'],
        'Session 2': ['2018-01-03', '2019-01-03']
    },
    114: {
        'Session 1': ['2015-01-06', '2015-12-18'],
        'Session 2': ['2016-01-03', '2017-01-03']
    },
    113: {
        'Session 1': ['2013-01-03', '2014-01-03'],
        'Session 2': ['2014-01-03', '2014-12-16']
    },
    112: {
        'Session 1': ['2011-01-05', '2012-01-03'],
        'Session 2': ['2012-01-03', '2013-01-03']
    },
    111: {
        'Session 1': ['2009-01-06', '2009-12-24'],
        'Session 2': ['2010-01-05', '2010-12-22']
    },
    110: {
        'Session 1': ['2007-01-04', '2007-12-31'],
        'Session 2': ['2008-01-03', '2009-01-03']
    },
    109: {
        'Session 1': ['2005-01-04', '2005-12-22'],
        'Session 2': ['2006-01-03', '2006-12-09']
    },
    108: {
        'Session 1': ['2003-01-04', '2003-12-09'],
        'Session 2': ['2004-01-20', '2004-12-08']
    },
    107: {
        'Session 1': ['2001-01-03', '2001-12-20'],
        'Session 2': ['2002-01-23', '2002-11-22']
    }
}


class Members_DataProcessor(DataProcessor):
    def __init__(self, batch_size):
        super(Members_DataProcessor, self).__init__(batch_size)
        self.data_path = Data.processor_members_dir
        self.table = "members"

    def to_csv(self):
        pass

    def process_data(self):
        pass

    def process_UK(self):
        pass

    def process_IL(self):
        pass

    def process_USA(self):
        # TODO read the file from folder
        file_path = os.listdir(self.data_path + '/USA')

        if len(file_path) > 0:
            data = Data.load_json(self.data_path + '/USA/' + file_path[0])
        else:
            print("No data to process")
            return

        to_write = []
        for key, value in data.items():
            members = value["results"][0]["members"]
            file_name = os.path.basename(file_path[0])
            name_parts = file_name.split('_')
            congress_num = name_parts[0]
            valid_from = converter[eval(congress_num)]["Session 1"][0]
            valid_until = converter[eval(congress_num)]["Session 2"][1]
            chamber = key
            counter = 0
            for member in members:
                id = member["id"]
                db_id = counter
                counter += 1
                name = member["first_name"] + " " + member["last_name"]
                country = 1
                party = member["party"]
                to_write.append([name, id, party,chamber, valid_from, valid_until, country])  # TODO make party id

        x = str(datetime.now()).replace(':', "-")
        csv_file_path = f"{Data.csv_files_dir}/members/{file_path[0]}_{x}.csv"

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "id", "party_id","chamber", "startDate", "endDate", "country"])
            writer.writeheader()

            writer = csv.writer(csvfile)
            writer.writerows(to_write)

            print("CSV file has been created successfully.")

        if os.path.exists(self.data_path + '/USA/' + file_path[0]):
            os.remove(self.data_path + '/USA/' + file_path[0])

    def process_TN(self):
        pass

    def process_CA(self):
        file_path = os.listdir(self.data_path + '/CA')

        # if dir is empty then exit
        if len(file_path) > 0:
            members = Data.load_json(self.data_path + '/CA/' + file_path[0])
        else:
            print('processor (CA members) did not find files to process')
            return

        # Open the CSV file for writing
        with open(f'{Data.csv_files_dir}/members/{file_path}.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["name", "party_id", "startDate", "endDate",
                                                          "country"])
            writer.writeheader()

            writer.writerows(members)

        if os.path.exists(self.data_path + '/CA/' + file_path[0]):
            os.remove(self.data_path + '/CA/' + file_path[0])
