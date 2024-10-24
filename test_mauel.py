from DiskManager import DiskManager  
from DBConfig import DBConfig
import os

class MyClass:
    def __init__(self, name):
        self.name = name


db_config=DBConfig.load_db_config("./config.txt")
disk_manager =DiskManager(db_config)



newpage=disk_manager.AllocPage()
print(newpage)
disk_manager.WritePage(newpage, b"Hello, World!")

bytearray1 = bytearray()
disk_manager.ReadPage(newpage,bytearray1)
print(bytearray1)

disk_manager.DeallocPage(newpage)

nextpage=disk_manager.AllocPage()

