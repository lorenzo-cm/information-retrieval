import logging

# Error logger
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('errors.out', mode='w')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
error_logger.addHandler(file_handler)

# Progress logger
progress_logger = logging.getLogger('progress_logger')
progress_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('progress.out', mode='w')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
progress_logger.addHandler(file_handler)