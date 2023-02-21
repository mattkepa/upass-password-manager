from configparser import ConfigParser

def db_config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        for key, value in parser.items(section):
            config[key] = value
    else:
        raise Exception(f'ConfigFile: Section {section} not found in {filename} file')

    return config
