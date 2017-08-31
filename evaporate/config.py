import ConfigParser
import os
from sys import exit


def get_option(option, option_type='str'):
    """
    Grabs the value of the option from the config file and returns it in the
    format requested.
    """

    option_value = config.get(get_section_name(), option)
    if option_type == 'str':
        return option_value
    elif option_type == 'str_list':
        return option_value.split(',')
    elif option_type == 'int_list':
        return map(int, option_value.split(','))


def get_section_name():
    """
    Returns name of the section in the config file.
    """
    return 'Evaporate'


def get_path(path_type=None, add=None):
    """
    Can return the base path on its own, or can add either of the following to
    it:
        * "mp3"
        * Second argument
        * "mp3" + second argument
    """
    path = get_option('PATH')
    if not os.path.isdir(path):
        print 'Path "' + path + '" does not exist.'
        exit()
    if path_type == 'mp3':
        path = os.path.join(path, 'mp3')
    if add:
        path = os.path.join(path, add)
    return path


def get_db_path():
    path = get_path(None, get_option('DB_FILENAME'))
    return path


def check_config_file():
    """
    Check if the config file exists, exits otherwise.
    """
    if not os.path.isfile(CONFIG_FILE):
        print 'Config file not found. Exiting...'
        exit()


CONFIG_FILE = os.path.abspath(os.path.join(os.getenv("HOME"),
                                           '.evaporate/config.cfg'))
check_config_file()
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
