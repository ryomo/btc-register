from configparser import ConfigParser

from run import APP_PATH


class Config(ConfigParser):

    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        self._config_path = config_path
        self.read([
            APP_PATH + '/config/app_default.ini',
            self._config_path,
        ])

    def write(self, **kwargs):
        with open(self._config_path, 'w') as configf_file:
            super().write(configf_file, **kwargs)
