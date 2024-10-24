import struct


class ColInfo:
    def __int__(self, nom, type):
        self.nom = nom
        self.type = type

    def get_nom(self):
        return self.nom

    def get_type(self):
        return self.type

class Relation :
    def __init__(self, nom, colonne):
        self.nom = nom
        self.colonne = colonne

    def get_column_names(self):
        return [col.nom for col in self.colonne]

    def get_column_types(self):
        return [col.type for col in self.colonne]

    def writeRecordToBuffer(self, record, buff, pos):
        start_pos = pos
        offset_directory = []
        for i, (col, val) in enumerate(zip(self.colonne, record.valeurs)):
            col_type = col.type
            offset_directory.append(pos - start_pos)

            if col_type == 'INT':
                buff[pos:pos + 4] = struct.pack('i', int(val))
                pos += 4
            elif col_type == 'REAL':
                buff[pos:pos + 4] = struct.pack('f', float(val))
                pos += 4
            elif col_type.startswith('CHAR'):
                char_size = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                encoded_value = val.encode('utf-8')[:char_size]
                buff[pos:pos + char_size] = encoded_value.ljust(char_size, b'\x00')
                pos += char_size
            elif col_type.startswith('VARCHAR'):
                char_size = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                encoded_value = val.encode('utf-8')
                length = len(encoded_value)
                if length > char_size:
                    raise ValueError(f"Valeur trop longue pour la colonne {col.name} (max {char_size} caractères)")
                buff[pos:pos + length] = encoded_value
                pos += length

        offset_directory.append(pos - start_pos)
        for offset in offset_directory:
            buff[start_pos:start_pos + 4] = struct.pack('i', offset)
            start_pos += 4
        return pos - start_pos

    def readFromBuffer(self, record, buff, pos):
        start_pos = pos
        record.valeurs = []
        for col in self.colonne:
            col_type = col.type
            if col_type == 'INT':
                val = struct.unpack('i', buff[pos:pos + 4])[0]
                record.valeurs.append(val)
                pos += 4
            elif col_type == 'REAL':
                val = struct.unpack('f', buff[pos:pos + 4])[0]
                record.valeurs.append(val)
                pos += 4
            elif col_type.startswith('CHAR'):
                char_size = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                val = buff[pos:pos + char_size].decode('utf-8').rstrip('\x00')
                record.valeurs.append(val)
                pos += char_size
            elif col_type.startswith('VARCHAR'):
                char_size = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                end_pos = pos + char_size
                val = buff[pos:end_pos].decode('utf-8').rstrip('\x00')
                record.valeurs.append(val)
                pos = end_pos

        return pos - start_pos
