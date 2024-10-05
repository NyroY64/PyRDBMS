import os

class DiskManager:
    def __init__(self, dbc):
      self.dbc=dbc
      
    
    def AlocPage():
        self.loadState()
        # if the list of free pages is not empty
        if not self.free_pages:
          free_page=self.free_pages.pop(0)
          return PageId(free_page[0], free_page[1])
          
        else:
            try:
                #we check the last file
                files=os.listdir(f"./{self.dbc.dbpath}/BinData")
                last_file = files[-1]
                
                #we check if the last file is not full
                with open(f"./{self.dbc.dbpath}/BinData/F{last_file}.rsdb", "rb") as fichier:
                    if len(fichier.read()) < self.dbc.dm_maxfilesize:
                        return PageId(last_file, len(fichier.read())//self.dbc.pageSize)
                    elif len(fichier.read()) == self.dbc.dm_maxfilesize:
                        #we alcate space in the file
                        with open(f"./{self.dbc.dbpath}/BinData/F{last_file}.rsdb", "ab") as fichier:
                            fichier.write(b'\x00' * self.dbc.pageSize)
                            return PageId(last_file, len(fichier.read())//self.dbc.pageSize)
                    else:
                        #we create a new file
                        with open(f"./{self.dbc.dbpath}/BinData/F{last_file+1}.rsdb", "wb") as fichier:
                            fichier.write(b'\x00' * self.dbc.pageSize)  # Init the file with one empty page
                            return PageId(last_file + 1, 0)
            except Exception as openFail:
                print(f"erreur d'ouverture de fichier = {openFail}")            
                
            
        
    def DeallocPage (pageId):
        self.free_pages.append(pageId)
        self.saveState()
            
            
        
    
    def ReadPage(self, pageID, buff):
        try:
            with open(f"./{self.dbc.dbpath}/BinData/F{pageID.FileIdx}.rsdb", "rb") as fichier:
                fichier.seek(self.dbc.pageSizepageID.PageIdx)
                buff = bytearray(fichier.read(self.dbc.pageSize))

        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")
            
            
            
    def WritePage(self, pageID, buff):
        try:
            with open(f"./{self.dbc.dbpath}/BinData/F{pageID.FileIdx}.rsdb", "wb") as fichier:
                fichier.seek(self.dbc.pageSizepageID.PageIdx)
                fichier.write(buff)

        except Exception as openFail:
            print(f"erreur d'ouverture de fichier = {openFail}")
            
            
            
    def SaveState(self):
       try:
           with open(f"./{self.dbc.dbpath}/dm.save","w") as fichier:
               for element in self.free_pages:
                   fichier.write(element.encode('utf-8') + b'\n')
       except Exception as openFail:
           print(f"erreur d'ouverture de fichier = {openFail}")       
  
    def LoadState(self):
       try:
           with open(f"./{self.dbc.dbpath}/dm.save", "rb") as fichier:
               contenu = fichier.readlines()
               self.free_pages = [ligne.decode('utf-8').strip() for ligne in contenu]
       except Exception as openFail:
           print(f"erreur d'ouverture de fichier = {openFail}")
              
                
          
        