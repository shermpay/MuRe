# Sherman Pay Jing Hao
# Thursday, 17. July 2014
# Functions to interact Mure conifiguration files

# List of Configuration vars.
config_vars = ['url', 'port', 'services', 'service_root', 'method', 'params']

def setup_config_env(config_vars):
    return {v: v for v in config_vars}

def read_config(file_path):
    """
    read_config(file_path) -> dict
    Reads config from file_path
    Returns a dict that holds the configuration
    """
    with open(file_path) as config_file:
        config_dict = eval(config_file.read(), setup_config_env(config_vars))
        return config_dict

def requesters(config):
    """
    get_requesters(config) -> set
    Returns a set of requesters
    """
    return config.keys()

def get_requester(config, requester):
    """
    request_config(config, requester) -> dict
    Returns a particular configuration for a requester given the config_dict
    """
    return config[requester]
