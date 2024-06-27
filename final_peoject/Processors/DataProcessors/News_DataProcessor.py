from Processors.DataProcessors.DataProcessor import DataProcessor


class News_DataProcessor(DataProcessor):
    def __init__(self, batch_size):
        super(News_DataProcessor, self).__init__(batch_size)
        self.data_path = Data.processor_news_dir

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
        file_path = os.listdir(self.data_path + '/USA')
        if len(file_path) >= 1:
            data = Data.load_json(self.data_path + '/USA/' + file_path[0])
        else:
            print("No data to process")
            return
        for new in data:
            content = new["abstract"]

    def process_TN(self):
        pass

    def process_CA(self):
        pass
