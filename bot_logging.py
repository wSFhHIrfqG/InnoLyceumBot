import logging.config
import logging

from config_data import log_config

# Конфигурируем логирование, инициализируем логгер
logging.config.dictConfig(log_config.LOG_CONFIG)
logger = logging.getLogger('logger')
