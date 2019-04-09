from configparser import ConfigParser

from run import APP_PATH


class Config(ConfigParser):

    def __init__(self, app_conf_path, **kwargs):
        super().__init__(**kwargs)

        default_conf_path = APP_PATH + '/config/app_default.ini'
        self._app_conf_path = app_conf_path
        user_conf_path = '/boot/btc-register-config/settings.ini'

        self.read([
            default_conf_path,
            self._app_conf_path,
            user_conf_path,
        ])

    def write(self, **kwargs):
        with open(self._app_conf_path, 'w') as config_file:
            super().write(config_file, **kwargs)
