# gunicorn.conf
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

# gevent setting
worker_class = 'gevent' 

# max_processes
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 
graceful_timeout = 100
timeout = 120