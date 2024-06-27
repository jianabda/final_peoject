from Collectors.DataCollectors.CA_DataCollector import CA_DataCollector
# from Collectors.DataCollectors.IL_DataCollector import IL_DataCollector
# from Collectors.DataCollectors.TN_DataCollector import TN_DataCollector
# from Collectors.DataCollectors.UK_DataCollector import UK_DataCollector
from Collectors.DataCollectors.USA_DataCollector import USA_DataCollector
from Collectors.NewsCollectors.IL_NewsCollector import IL_NewsCollector
from Collectors.NewsCollectors.USA_NewsCollector import USA_NewsCollector
from Collectors.NewsCollectors.UK_NewsCollector import UK_NewsCollector
from Collectors.NewsCollectors.CA_NewsCollector import CA_NewsCollector


class CollectorManager:
    def __init__(self, batch_size):
        self.batch_size = batch_size

        self.collectors = [CA_DataCollector(batch_size)]

    def run_collectors(self):
        for collector in self.collectors:
            # collector.get_news()
            collector.get_debates()
            # collector.get_bills()
            # collector.get_members()
