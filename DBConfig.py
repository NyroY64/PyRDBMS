import json

class DBConfig:
    def __init__(self, dbpath):
        self.dbpath = dbpath

        
    def load_db_config(file_path):
        config=None
        
        with open(file_path, 'r') as file:
            config=json.load(file)
            config= config["dbms_settings"]["dbpath"]
            return config
            
        
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
         
        

