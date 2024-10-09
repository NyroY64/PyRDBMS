import json
import os 

class DBConfig:
    def __init__(self, dbpath ,pageSize ,dm_maxfilesize, bm_buffercount, bm_policy):
        self.dbpath = dbpath
        self.pageSize=pageSize
        self.dm_maxfilesize=dm_maxfilesize
        self.bm_buffercount=bm_buffercount
        self.bm_policy=bm_policy
    

    def get_dbpath(self):
        return self.dbpath

    def set_dbpath(self, dbpath):
        self.dbpath = dbpath

    def get_pageSize(self):
        return self.pageSize

    def get_dm_maxfilesize(self):
        return self.dm_maxfilesize

    def get_bm_buffercount(self):
        return self.bm_buffercount

    def get_bm_policy(self):
        return self.bm_policy

    def load_db_config(file_path):
        
        try:
            with open(file_path, 'r') as file:
                config=json.load(file)

                return DBConfig(config["dbpath"] ,config["pageSize"] ,config["dm_maxfilesize"], config["bm_buffercount"], config["bm_policy"])
            
        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")

            
