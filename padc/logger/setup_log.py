from pathlib import Path
import logging
import logging.config

settings_path = Path.joinpath(Path(__file__).parent.parent, Path('config/logging_settings.ini'))
print(settings_path)
logging.config.fileConfig(settings_path)
logger = logging.getLogger('root')
