from pathlib import Path
import logging
import logging.config


log_path = Path.joinpath(Path(__file__).parent.parent.parent, 'loggin_settings.ini')
logging.config.fileConfig('logging_settings.ini')
logger = logging.getLogger('root')
