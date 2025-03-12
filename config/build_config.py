
import configparser


def read_api_key():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['discordapi']['token']


def read_dbname():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['postgres']['dbname']


def read_dbuser():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['postgres']['dbuser']


def read_dbpass():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['postgres']['dbpass']
