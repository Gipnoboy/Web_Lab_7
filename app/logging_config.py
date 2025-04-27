import logging
import logging.handlers
import os

def setup_logging():
    """Налаштовує логування із збереженням у файл та виводом у консоль"""
    logger = logging.getLogger("api_requests")
    logger.setLevel(logging.INFO)

    # Формат логів
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Обробник для файлу (з ротацією)
    log_file = "api.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1048576, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обробник для консолі
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)