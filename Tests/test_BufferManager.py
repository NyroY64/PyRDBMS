import unittest
from unittest.mock import MagicMock


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BufferManager import BufferManager
from BufferManager import BufferManager
from pageId import PageId
from DiskManager import DiskManager


class TestBufferManager(unittest.TestCase):

    def setUp(self):
        # Mock database configuration
        self.mock_db_config = MagicMock()
        self.mock_db_config.bm_buffercount = 5
        self.mock_db_config.bm_policy = "LRU"
        
        # Mock DiskManager
        self.mock_disk_manager = MagicMock(spec=DiskManager)
        self.mock_disk_manager.ReadPage.return_value = bytearray([0]*100)
        
        # Create an instance of BufferManager
        self.buffer_manager = BufferManager(self.mock_db_config, self.mock_disk_manager)

    def test_GetPage_new_page(self):
        # Test fetching a new page that is not in the buffer pool
        page_id = PageId(FileIdx=1, PageIdx=2)
        buffer_index = self.buffer_manager.GetPage(page_id)
        
        self.assertIsInstance(buffer_index, int)
        self.assertEqual(buffer_index, 0)  # Expected to load into first available slot
        self.mock_disk_manager.ReadPage.assert_called_once_with(page_id)

    def test_GetPage_existing_page(self):
        # Test fetching a page already in the buffer pool
        page_id = PageId(FileIdx=1, PageIdx=2)
        self.buffer_manager.GetPage(page_id)  # Load the page
        self.mock_disk_manager.ReadPage.reset_mock()  # Reset mock calls
        
        buffer_index = self.buffer_manager.GetPage(page_id)
        self.assertEqual(buffer_index, 0)  # Same buffer slot as before
        self.mock_disk_manager.ReadPage.assert_not_called()

    def test_GetPage_LRU_policy(self):
        # Test the LRU replacement policy
        self.mock_db_config.bm_policy = "LRU"
        
        # Fill the buffer
        for i in range(self.mock_db_config.bm_buffercount):
            page_id = PageId(FileIdx=1, PageIdx=i)
            self.buffer_manager.GetPage(page_id)
        
        # Access the first page to make it "recently used"
        self.buffer_manager.GetPage(PageId(FileIdx=1, PageIdx=0))
        
        # Add a new page, triggering LRU
        new_page_id = PageId(FileIdx=2, PageIdx=99)
        buffer_index = self.buffer_manager.GetPage(new_page_id)
        
        self.assertNotEqual(buffer_index, 0)  # Should replace an older page
        self.assertEqual(buffer_index, 1)    # Based on LRU logic

    def test_FreePage(self):
        # Test freeing a page from the buffer pool
        page_id = PageId(FileIdx=1, PageIdx=2)
        buffer_index = self.buffer_manager.GetPage(page_id)
        
        self.buffer_manager.FreePage(page_id, valdirty=False)
        # Since pin_count is decremented, ensure the page is still valid in the buffer pool
        buffer = self.buffer_manager.buffer_pool[buffer_index]
        self.assertEqual(struct.unpack('i', buffer[:4])[0], page_id.FileIdx)
        self.assertEqual(struct.unpack('i', buffer[4:8])[0], page_id.PageIdx)

    def test_lru(self):
        # Direct test for LRU policy
        self.mock_db_config.bm_policy = "LRU"
        
        # Fill the buffer with test pages
        for i in range(self.mock_db_config.bm_buffercount):
            page_id = PageId(FileIdx=1, PageIdx=i)
            self.buffer_manager.GetPage(page_id)
        
        # Trigger LRU replacement
        lru_index = self.buffer_manager.lru()
        self.assertNotEqual(lru_index, -1)  # Ensure a valid index is returned

    def test_mru(self):
        # Direct test for MRU policy
        self.mock_db_config.bm_policy = "MRU"
        
        # Fill the buffer with test pages
        for i in range(self.mock_db_config.bm_buffercount):
            page_id = PageId(FileIdx=1, PageIdx=i)
            self.buffer_manager.GetPage(page_id)
        
        # Trigger MRU replacement
        mru_index = self.buffer_manager.mru()
        self.assertNotEqual(mru_index, -1)  # Ensure a valid index is returned

if __name__ == '__main__':
    unittest.main()
