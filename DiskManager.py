class DiskManager:
    def __init__(self, (db_config):
      self.db_config=db_config

     def __repr__(self):
        """
        Représentation de l'objet DiskManager pour l'affichage.
        """
        return f"DiskManager(db_config={self.db_config})"
