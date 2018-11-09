import os
import json
import logging.config

"""Envrionment Variable LOG_CFG=my_logging.json python file.py """

def setup_logging(default_path='logging_config.json', default_level=logging.INFO, env_key='LOG_CFG'):

	"""
	Setups logging configuration parameters.

	Args:
		default_path: Location of JSON configuration file.
		default_level: Default logging level [DEBUG |INFO | WARNING | ERROR | CRITICAL].
		env_key: Name of envirionment variable used to store logging configuration location

	Returns:
		None.

	Raises:
		None.
	"""
	
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
