import yaml

botOptions = ['token', 'prefix', 'name', 'adminrank', 'channel_member_count', 'channel_new_user', 'embed_color']
mtaOptions = ['ip', 'port']

def configCheck(data):
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)

        if data in botOptions:
            return cfg["bot"][data]
        elif data in mtaOptions:
            return cfg["mta"][data]