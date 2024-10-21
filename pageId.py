class PageId:
    def __init__(self, FileIdx, PageIdx):
        self.FileIdx = FileIdx
        self.PageIdx = PageIdx
    
    def __repr__(self):
        return f"PageId(FileIdx={self.FileIdx}, PageIdx={self.PageIdx})"