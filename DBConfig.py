import json
import os 

class DBConfig:
    def __init__(self, dbpath):
        self.dbpath = dbpath

    def get_dbpath(self):
        return self.dbpath

    def set_dbpath(self, dbpath):
        self.dbpath = dbpath
        
    def load_db_config(file_path):
        config=None
        
        with open(file_path, 'r') as file:
            config=json.load(file)
            config= config["dbpath"]
            if config:
                return DBConfig(chemin)
            else:
                raise IOError("The configuration file is empty or contains an invalid path.")
            
        
        # try:
        #     file = open(file_path, 'r')
        #     config=file.read()
        #     print(config)
        #     for line in file:
        #         if line.startswith('dbpath'):
        #             _, path = line.split('=')
        #             config= DBConfig(dbpath=path.strip().strip("\""))
        #             return config
        # finally:
        #     file.close()
         
        

