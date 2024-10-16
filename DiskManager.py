from PageId import PageId 
class DiskManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.free_pages = []  # Liste de pages libres, chaque élément est un objet PageId
        self.file_sizes = []  # Liste pour stocker la taille de chaque fichier (nombre d'octets)

    def __repr__(self):
        """
        Représentation de l'objet DiskManager pour l'affichage.
        """
        return f"DiskManager(db_config={self.db_config})"
    
    def AllocPage(self):
        """
        Alloue une nouvelle page, soit en réutilisant une page libre, soit en ajoutant une page à la fin d'un fichier.
        :return: Un PageId correspondant à la page allouée.
        """
        # 1. Vérifier s'il existe des pages désallouées dans la liste des pages libres
        if self.free_pages: #Liste n'est pas vide 
            # Si une page libre est disponible, la récupérer et la retirer de la liste
            page_id = self.free_pages.pop()
            return page_id  # Retourner le PageId correspondant à la page réutilisée

        # 2. Sinon, trouver un fichier qui n'a pas atteint sa taille maximale
        for file_idx, file_size in enumerate(self.file_sizes):   # récupérer le couple (indice,element de la liste file size)
            if file_size + self.db_config.pagesize <= self.db_config.dm_maxfilesize:
                # Le fichier a encore de la place, on peut ajouter une nouvelle page à la fin
                page_idx = file_size // self.db_config.pagesize  # Calcul de l'indice de la nouvelle page
                self.file_sizes[file_idx] += self.db_config.pagesize  # Mettre à jour la taille du fichier dans la liste
                return PageId(file_idx, page_idx)  # Retourner le PageId correspondant à la nouvelle page allouée

        # 3. Si tous les fichiers ont atteint leur taille maximale, créer un nouveau fichier
        new_file_idx = len(self.file_sizes)  # Le nouvel indice du fichier (correspond à la longueur actuelle de la liste)
        self.file_sizes.append(self.db_config.pagesize)  # Ajouter le nouveau fichier avec une page allouée (pagesize octets)
        return PageId(new_file_idx, 0)  # La première page (indice 0) dans le nouveau fichier

     
