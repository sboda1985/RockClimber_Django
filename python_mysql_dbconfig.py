from configparser import ConfigParser


def read_db_config(filename='/home/pi/python_mysql_config_file/config.ini'):
    """ Read the hostname, username, passwd and database and return it
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
    
    # get parameters
    return parser.get('django', 'password')


