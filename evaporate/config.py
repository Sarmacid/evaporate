import ConfigParser
import os

CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '../config/config.cfg'))
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)


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
    return 'Evaporate'


def get_path(path_type=None, add=None):
    path = os.path.join(os.getenv("HOME"), 'evaporate')
    if path_type == 'mp3':
        path = os.path.join(path, 'mp3')
    if add:
        path = os.path.join(path, add)
    return path


def get_db_path():
    path = get_path(None, get_option('DB_FILENAME'))
    return path
