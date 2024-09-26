from DBConfig import DBConfig

if __name__ == "__main__":
    config = DBConfig.load_db_config('config.txt')
    print(config)
