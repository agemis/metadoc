import os
import pymongo
from pymongo import MongoClient

import config as cfg

class DatabaseLibrary:
    client = MongoClient(cfg.database["uri"])
    db = client[cfg.database["db"]]
    collection = db[cfg.database["collection"]]


                       
        
