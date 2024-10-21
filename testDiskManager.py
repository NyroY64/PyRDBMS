import unittest
import os
from DiskManager import DiskManager  
from pageId import pageId  # Ensure pageId is a class, not a module


class MockDbc:
    def __init__(self, dbpath, dm_maxfilesize, pageSize):
        self.dbpath = dbpath
        self.dm_maxfilesize = dm_maxfilesize
        self.pageSize = pageSize

class TestDiskManager(unittest.TestCase):

    def setUp(self):
        # Set up the mock database configuration (dbc) and DiskManager instance
        self.dbc = MockDbc(dbpath="test_db", dm_maxfilesize=4096, pageSize=512)
        self.disk_manager = DiskManager(self.dbc)

        # Ensure the directory structure for the test
        os.makedirs(f"./{self.dbc.dbpath}/BinData", exist_ok=True)
        self.disk_manager.free_pages = []  # Start with an empty list of free pages
    
    def tearDown(self):
        # Cleanup after tests
        if os.path.exists(f"./{self.dbc.dbpath}/dm.save"):
            os.remove(f"./{self.dbc.dbpath}/dm.save")
        if os.path.exists(f"./{self.dbc.dbpath}/BinData"):
            for file in os.listdir(f"./{self.dbc.dbpath}/BinData"):
                os.remove(f"./{self.dbc.dbpath}/BinData/{file}")
            os.rmdir(f"./{self.dbc.dbpath}/BinData")
        os.rmdir(f"./{self.dbc.dbpath}")

    def test_alloc_page(self):
        # Simulate the allocation of a page when there are no free pages
        page = self.disk_manager.AllocPage()
        self.assertIsNotNone(page, "AllocPage should return a valid page")

    
if __name__ == '__main__':
    unittest.main()
