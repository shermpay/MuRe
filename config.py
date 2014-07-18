# Sherman Pay Jing Hao
# Thursday, 17. July 2014

"""
Module for config objects
"""

class Config(object):
    """
    Used for interacting with a particular Mure configuration file.
    Allows easy access and reading of the configuration file.
    Example Config:
    {
        'test1': {url: "http://mure.com",
                  port: 8080,
                  service_root: "/hello",
                  services: {"/foo": {params: [['user_name', "id"], 
                                                ["guido", "14"],
                                                ["shermpay", "13"]],
                                               method: GET},
                            "/bar": {params: [['user_name'],
                                                ["guido"]],
                                                method: POST},
                             }
                  }
    }
    """

    # List of Configuration keys.
    config_keys = ['url', 'port', 'services', 'service_root', 'method', 'params'
                   'GET', 'POST']

    def __init__(config_file):
        setup_env(config_keys)

    def setup_env(config_keys):
        """
        Setup the environment of configuration
        """
        return {v: v for v in config_keys}
        
    def read_file(file_path):
        """
        read_file(file_path) -> dict
        Reads config from file_path
        Returns a dict that holds the configuration
        """
        with open(file_path) as config_file:
            config_dict = eval(config_file.read(), setup_config(config_vars))
            return config_dict

    def requesters(self):
        """
        get_requesters(config) -> set
        Returns a set of requesters
        """
        return config.keys()

    def get_requester(requester):
        """
        request_config(config, requester) -> dict
        Returns a particular configuration for a requester given the config_dict
        """
        return self[requester]
