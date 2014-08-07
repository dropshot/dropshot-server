import yaml


class Config:
    """
    Config

    Defines a config, its attributes, and the methods that act on it.

    Attributes:
        Various. Attributes are defined by parameters from the YAML-formatted
        config file passed into the __init__ method.
    """

    def __init__(self, config_file, config_name):
        """
        Initializes the instance with the named config found in the config file
        by calling _load_config.

        Args:
            self
            config_file: The file from from which to load configs.
            config_name: The name of the config to load from the config file.

        Returns:
            none
        """

        self._load_config(config_file, config_name)

    def _load_config(self, config_file, config_name):
        """
        Loads a config from a config file.

        Args:
            self
            config_file: The file from from which to load configs.
            config_name: The name of the config to load from the config file.

        Returns:
            none
        """

        with open(config_file) as cf:
            configs = yaml.load(cf)
            try:
                self.__dict__.update(configs[config_name])
            except KeyError:
                print('dropshot: could not load config ({}). '
                      'no such config.'.format(config_name))
