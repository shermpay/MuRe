""" Configuration Parser and Evaluator"""
# Sherman Pay Jing Hao
# Thursday, 17. July 2014

from enum import Enum

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
    
    # Enumeration of Configuration keys.
    TargetKey = Enum('TargetKey', 'url port services service_root')
    ServiceKey = Enum('ServiceKey', 'method params GET POST times')
    ConfKey = Enum('ConfKey', 'targets ordering')

    def __init__(self, config_file):
        env = self.setup_env()
        self.config = self.read_file(config_file, env)

    def setup_env(self):
        """
        Setup the environment of configuration
        This will allow usage of unquoted variable like keywords in the config.
        """
        lst = [list(k) for k in [self.TargetKey, self.ServiceKey, self.ConfKey]]
        
        return {key.name : key for keys in lst for key in keys}

    def read_file(self, file_path, env):
        """
        read_file(file_path) -> dict
        Reads config from file_path
        Returns a dict that holds the configuration
        """
        with open(file_path) as config_file:
            config_dict = eval(config_file.read(), env)
            return config_dict

    def requesters(self):
        """
        get_requesters(config) -> set
        Returns a set of requesters
        """
        return self.config.keys()

    def get_requester(self, requester):
        """
        request_config(config, requester) -> dict
        Returns a particular configuration for a requester given the config_dict
        """
        return self.config[requester]
