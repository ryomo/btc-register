from configparser import ConfigParser


class Config(ConfigParser):

    default_ini = """
[shop]
name = My Shop

[fiat]
name = USD

[btc]
price = GDAX(USD)

[lnd]
url = https://localhost:8080
cert_path = ~/.btc-register/tls.cert
macaroon_path = ~/.btc-register/admin.macaroon
"""

    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        self._config_path = config_path
        self.read_string(self.default_ini)
        self.read(self._config_path)

    def write(self, **kwargs):
        with open(self._config_path, 'w') as configf_file:
            super().write(configf_file, **kwargs)
