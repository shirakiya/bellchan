import time
from multiprocessing import Process


def parallel(job_function, *args):
    job_process = Process(target=job_function, args=args)
    job_process.start()

    while True:
        if job_process.is_alive():
            time.sleep(1)
        else:
            break

    job_process.terminate()
