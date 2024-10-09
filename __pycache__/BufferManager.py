class BufferManager:
    def __init__(self, db_config, disk_manager):
        self.db_config = db_config
        self.disk_manager = disk_manager
        self.buffer_pool = []

    def GetPage(self, pageId):
        for i, (pid, buffer) in enumerate(self.buffer_pool):
            if pid == pageId:
                self.buffer_pool.append(self.buffer_pool.pop(i))
                return buffer

        buffer = bytearray(self.db_config.pageSize)
        self.disk_manager.ReadPage(pageId, buffer)
        if len(self.buffer_pool) >= self.buffer_capacity:
            self.buffer_pool.pop(0)
        self.buffer_pool.append((pageId, buffer))

        return buffer


