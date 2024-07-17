# cat gunicorn_conf.py
import sys
import multiprocessing
import os
os.system("pip freeze ")
# See https://docs.gunicorn.org/en/stable/settings.html for details
# note parameters explicitly via gunicorn cmd line overrides what are set here
#  e.g. even though default here is info, "gunicorn --log-level=debug -c [this file]
#       would mean the debug level is debug, not info


LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", '1')
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "80")

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)

default_web_concurrency = workers_per_core * cores
web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
workers = web_concurrency
worker_class = 'uvicorn.workers.UvicornWorker'
bind = f"{host}:{port}"
keepalive = os.getenv("GUNICORN_KEEPALIVE", 120)
errorlog = "-"
threads = os.getenv("GUNICORN_THREADS", 120)


def worker_int(worker) -> None:
    sys.exit(1)


def child_exit(server, worker) -> None:
    sys.exit(1)
