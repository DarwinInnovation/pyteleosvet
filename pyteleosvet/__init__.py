from pyteleosvet.update_run import *
from pyteleosvet.day_figures import *

import json

__version__ = "0.1.0"

class TeleosError(Exception):
    """Exception raised for errors in Teleos module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class Teleos(object):
    def __init__(self, config_path):
        self._config_path = config_path
        self._config = dict()

        self._load_config()
        self._cfg_db_televet()
        self._cfg_db_dvc()

    def _load_config(self):
        with open(self._config_path, 'rb') as cfg_fp:
            cfg = json.load(cfg_fp)

        self._config = cfg

    def _cfg_db_televet(self):
        if 'teleos' not in self._config:
            raise TeleosError('No teleos database configuration')

        teleos_cfg = self._config['teleos']

        if not 'mysql' in teleos_cfg:
            raise TeleosError('Bad database configuration')

        teleos_db_cfg = teleos_cfg['mysql']

        teleos_db = get_teleos_db()
        teleos_db.init(**teleos_db_cfg)

    def _cfg_db_dvc(self):
        dvc_cfg = self._config['dvc']

        if not 'mysql' in dvc_cfg:
            raise TeleosError('Bad database configuration')

        dvc_db_cfg = dvc_cfg['mysql']

        dvc_db = get_dvc_db()
        dvc_db.init(**dvc_db_cfg)


teleos = None

def init(config_file):
    teleos = Teleos(config_file)

    return teleos
