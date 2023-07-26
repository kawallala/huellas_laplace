import logging
from logging.handlers import TimedRotatingFileHandler
import os 

def create_logs():
    # Create a "logs" folder if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Set up the app_logger
    app_logger = logging.getLogger('app_log')
    app_logger.setLevel(logging.DEBUG)

    # Create a TimedRotatingFileHandler for app_logger
    file_handler_app = TimedRotatingFileHandler('logs/app_log_file.log', when='midnight', interval=1, backupCount=0)  # backupCount=0 means infinite backups

    # Create a formatter (optional)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler_app.setFormatter(formatter)

    # Add the handler to the app_logger
    app_logger.addHandler(file_handler_app)

    # Set up the person_logger
    person_logger = logging.getLogger('person_log')
    person_logger.setLevel(logging.DEBUG)

    # Create a TimedRotatingFileHandler for person_logger
    file_handler_person = TimedRotatingFileHandler('logs/person_log_file.log', when='midnight', interval=1, backupCount=0)  # backupCount=0 means infinite backups

    # Set the formatter for person_logger
    file_handler_person.setFormatter(formatter)

    # Add the handler to the person_logger
    person_logger.addHandler(file_handler_person)

    # Now both loggers will use TimedRotatingFileHandler with daily rotation and infinite backups,
    # and the log files will be placed inside the "logs" folder.
    return [app_logger, person_logger]
