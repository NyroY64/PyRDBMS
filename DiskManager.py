
#--------------------------------AU DEBUT LA CLASSE DISKMANAGER MANIPULE DES ELEMNTS EN MEMOIRE (LISTE) DONC FICHIER ET PAGE--------------------------------------------------------
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


#------------------------------ON VEUT MAINTENANT QU'ELLE MANIPULE REELLEMENT DES FICHIERS BINAIRES SUR LE DISQUE DONC ON VA CREER ET OUVRIR DES FICHIERS BINAIRES SI C'EST NECESSAIRE -------------------------------------
import os
from PageId import PageId

class DiskManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.free_pages = []  # Liste des pages libres, chaque élément est un objet PageId
        self.file_sizes = []  # Liste pour stocker la taille de chaque fichier (nombre d'octets)
        self._initialize_storage()

    def _initialize_storage(self):
        """
        Crée le répertoire de stockage et prépare le sous-dossier BinData s'il n'existe pas déjà.
        """
        bin_data_path = os.path.join(self.db_config.dbpath, 'BinData')
        if not os.path.exists(bin_data_path):
            os.makedirs(bin_data_path)

    def _get_file_path(self, file_idx):
        """
        Retourne le chemin complet d'un fichier binaire donné (par exemple F0.rsdb, F1.rsdb).
        :param file_idx: L'indice du fichier.
        :return: Chemin complet du fichier correspondant.
        """
        return os.path.join(self.db_config.dbpath, 'BinData', f'F{file_idx}.rsdb')

    def _get_file_size(self, file_idx):
        """
        Retourne la taille du fichier en octets.
        :param file_idx: L'indice du fichier.
        :return: La taille du fichier en octets, ou 0 si le fichier n'existe pas.
        """
        file_path = self._get_file_path(file_idx)
        return os.path.getsize(file_path) if os.path.exists(file_path) else 0

    def AllocPage(self):
        """
        Alloue une nouvelle page en manipulant les fichiers binaires.
        :return: Un PageId correspondant à la page allouée.
        """
        # 1. Vérifier s'il existe des pages libres (désallouées)
        if self.free_pages:
            page_id = self.free_pages.pop()
            return page_id  # Retourner le PageId correspondant à la page réutilisée

        # 2. Rechercher un fichier qui n'a pas atteint sa taille maximale
        for file_idx in range(len(self.file_sizes)):
            file_size = self._get_file_size(file_idx)
            if file_size + self.db_config.pagesize <= self.db_config.dm_maxfilesize:
                # Le fichier a de la place, ajouter une nouvelle page
                page_idx = file_size // self.db_config.pagesize
                self._write_empty_page(file_idx, file_size)  # Ajouter physiquement la page au fichier
                return PageId(file_idx, page_idx)

        # 3. Créer un nouveau fichier si tous les fichiers sont pleins
        new_file_idx = len(self.file_sizes)
        new_file_size = 0
        self._write_empty_page(new_file_idx, new_file_size)  # Créer un nouveau fichier et ajouter une première page
        return PageId(new_file_idx, 0)  # La première page (indice 0)

    def _write_empty_page(self, file_idx, file_size):
        """
        Écrit une nouvelle page vide (remplie de zéros) à la fin d'un fichier binaire.
        :param file_idx: L'indice du fichier.
        :param file_size: La taille actuelle du fichier.
        """
        file_path = self._get_file_path(file_idx)

        # Ouvrir le fichier en mode lecture/écriture binaire. Le fichier est créé s'il n'existe pas.
        with open(file_path, 'a+b') as f:
            f.seek(file_size)  # Se positionner à la fin du fichier
            f.write(b'\x00' * self.db_config.pagesize)  # Écrire une page vide de taille pagesize

    def read_page(self, file_idx, page_idx):
        """
        Lit une page donnée depuis un fichier binaire.
        :param file_idx: L'indice du fichier.
        :param page_idx: L'indice de la page dans le fichier.
        :return: Le contenu de la page en tant que bytes.
        """
        file_path = self._get_file_path(file_idx)
        offset = page_idx * self.db_config.pagesize

        # Ouvrir le fichier en mode lecture binaire
        with open(file_path, 'rb') as f:
            f.seek(offset)  # Aller à la position de la page
            return f.read(self.db_config.pagesize)  # Lire et retourner la page

    

     
