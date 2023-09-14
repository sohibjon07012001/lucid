# gunicorn_conf.py
from multiprocessing import cpu_count

bind = "127.0.0.1:8002"

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/sohibjon/Local_Disck/Zypl/FastApi/access_log'
errorlog =  '/home/sohibjon/Local_Disck/Zypl/FastApi/error_log'