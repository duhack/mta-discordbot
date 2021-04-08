#AUTHOR: duhack
#GITHUB: https://github.com/duhack
#WWW: https://duhack.pl/ 

import yaml

botOptions = ['token', 'prefix', 'name', 'adminrank', 'channel_member_count', 'channel_new_user', 'embed_color', 'synchro_rank']
mtaOptions = ['ip', 'port']
mysqlOptions = ['host', 'user', 'database', 'password']

def configCheck(data):
    with open("config.yml", "r", encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile)

        if data in botOptions:
            return cfg["bot"][data]
        elif data in mtaOptions:
            return cfg["mta"][data]
        elif data in mysqlOptions:
            return cfg["mysql"][data]