import owncloud
import configparser

config = configparser.ConfigParser()

class OwncloudHelper:
    oc = None

    def __init__(self):
        config.read('config.ini')
        self.oc = owncloud.Client(config['owncloud']['URL'])
        self.oc.login(config['owncloud']['USER'],
                      config['owncloud']['PASSWORD'])