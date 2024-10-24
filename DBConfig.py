import json
import os 

class DBConfig:
    def __init__(self, dbpath ,pageSize ,dm_maxfilesize):
        self.dbpath = dbpath
        self.pageSize=pageSize
        self.dm_maxfilesize=dm_maxfilesize
    

    def get_dbpath(self):
        return self.dbpath

    def set_dbpath(self, dbpath):
        self.dbpath = dbpath
<<<<<<< Updated upstream
=======

    def get_pageSize(self):
        return self.pageSize

    def set_pageSize(self, pageSize):
        self.pageSize = pageSize

    def get_dm_maxfilesize(self):
        return self.dm_maxfilesize

    def set_dm_maxfilesize(self, dm_maxfilesize):
        self.dm_maxfilesize = dm_maxfilesize
>>>>>>> Stashed changes
        
        
    @staticmethod    
    def load_db_config(file_path):
        
        try:
            with open(file_path, 'r') as file:
                config=json.load(file)

                return DBConfig(config["dbpath"] ,config["pageSize"] ,config["dm_maxfilesize"])
            
        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")

            
        


