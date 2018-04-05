from multiprocessing import Process
import time


def parallel(job_function):
    job_process = Process(target=job_function)
    job_process.start()

    while True:
        if job_process.is_alive():
            time.sleep(1)
        else:
            break

    job_process.terminate()
