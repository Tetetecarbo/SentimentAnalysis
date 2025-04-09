import logging
import os
from datetime import datetime

# Configure logging
def setup_logging(log_file='app.log'):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_path = os.path.join('logs', log_file)
    
    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format='%(asctime)s, %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )

# Function to log an error
def log_error(message):
    logging.error(message)

# Function to log general information
def log_info(message):
    logging.info(message)

# Helper function to convert string to datetime
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        log_error(f"Error parsing date: {date_string} - {e}")
        return None

# Function to safely create a directory
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        log_info(f"Directory created: {directory}")
    else:
        log_info(f"Directory already exists: {directory}")

# Example usage of the utility functions
if __name__ == "__main__":
    setup_logging()
    ensure_dir('output')
    log_info("Application started")
    date = parse_date("204-01-01 12:00:00")
    if date:
        log_info(f"Date parsed successfully: {date}")