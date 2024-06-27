import os
from Data.GLOBAL import Data
from Collectors.CollectorManager import CollectorManager
from Processors.ProcessorManager import ProcessorManager
import json
from time import time

if __name__ == "__main__":

    collector_m = CollectorManager(15)

    processor_m = ProcessorManager(15)

    since = time()
    for i in range(70):
        collector_m.run_collectors()
        processor_m.run_processors()

    print(f"elapsed: {time() - since}")
