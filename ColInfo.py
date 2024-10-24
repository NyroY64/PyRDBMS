class ColInfo:
    def __init__(self, colNom, colType):
        self.colNom=colNom
        self.colType = colType

    def get_colNom(self):
        return self.colNom

    def set_colNom(self, colNom):
        self.colNom = colNom

    def get_colType(self):
        return self.colType

    def set_colType(self, colType):
        self.colType = colType