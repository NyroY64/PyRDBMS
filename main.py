from DBConfig import DBConfig

if __name__ == "__main__":
    config = DBConfig.load_db_config('config.txt')
    print(config.get_dbpath())

#T'as rien testé YOUCEFF t'as juste récupérer le chemin haha depuis un fichier.txt alors qu'on a chiisi deja un fichier.json pour la config !!!
