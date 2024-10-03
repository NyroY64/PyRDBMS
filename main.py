#!/usr/bin/env python3

from DBConfig import DBConfig


if __name__ == "__main__":
    print("Mon application est lancée !")
    config = DBConfig.load_db_config('config.txt')
    print(config.get_dbpath())
