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
        
        #Le type de méthode LoadDBConfig : Vous l'avez définie comme une méthode classique de la classe, mais elle n'utilise pas l'instance (self).
        #Cela signifie qu'elle devrait être définie comme une méthode statique (ou classe) en utilisant @staticmethod.......
    
    @staticmethod    
    def load_db_config(file_path):
        
        try:
            with open(file_path, 'r') as file:
                config=json.load(file)

                return DBConfig(config["dbpath"] ,config["pageSize"] ,config["dm_maxfilesize"])
            
        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")
        

