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
        
        try:
            with open(file_path, 'r') as file:
                config=json.load(file)
                configPath = config["dbpath"]
                return DBConfig(configPath)
        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")

            
        
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
         
        

